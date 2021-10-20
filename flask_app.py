
# A very simple Flask Hello World app for you to get started with...
from flask import Flask, request
from feed_forward_classifier import FeedForwardClassifier
from feed_forward_ner import FeedForwardNER
from response import Response
import MySQLdb
import time
from datetime import datetime
import gc

app = Flask(__name__)
gc.collect ()

ffc = FeedForwardClassifier (model_path = "/home/beinglabs/bighead/classifier_model.npz")
ffner = FeedForwardNER (model_path = "/home/beinglabs/bighead/ner_model.npz")

def get_date (timestamp):
    return datetime.utcfromtimestamp (timestamp).strftime('%b %d')

def get_time (timestamp):
    return datetime.utcfromtimestamp (timestamp).strftime('%H:%M')

def create_memory (user_id, sentence, keywords, response, conn, cursor):
    timestamp = time.time ()
    query = "INSERT INTO `tbl_memories` (`fld_id`, `fld_user_id`, `fld_sentence`, `fld_keywords`, `fld_timestamp`) VALUES (%s, %s, '%s', '%s', %d)" % ('NULL', user_id, sentence.replace ("'", "\\'"), keywords.replace ("'", "\\'"), timestamp)
    try:
        cursor.execute (query)
        conn.commit ()
        response.message = "Okay, I will remember that"
    except:
        conn.rollback ()
        response.message = "Something went wrong, please try again"

def get_memory (user_id, keywords, response, cursor):
    main_query = "SELECT `fld_sentence`, `fld_timestamp`, (0"
    sub_query = ""
    for word in keywords:
        sub_query = sub_query + " + (`fld_keywords` LIKE '%%%s%%')" % (word.replace ("'", "\\'"))
    main_query = main_query + sub_query + ") as global_hits FROM `tbl_memories` WHERE `fld_user_id` = " + user_id + " HAVING global_hits = (SELECT (0" + sub_query + ") as local_hits FROM `tbl_memories` HAVING local_hits > 0 ORDER BY local_hits DESC LIMIT 1) ORDER BY `fld_timestamp`;"
    if cursor.execute (main_query) > 1:
        count = 1
        result_set = cursor.fetchall ()
        response.message = "I remember you told me"
        for result_row in result_set:
            response.message = response.message + "\n #" + str (count) + " " + result_row[0].replace
            count = count + 1
            #response.message.append ({'date': get_date (result_row[1]), 'time': get_time (result_row[1]), 'sentence': result_row[0].replace ("\\'", "'")})
    elif cursor.execute (main_query) == 1:
        result_set = cursor.fetchall ()
        response.message = "I remember you told me"
        for result_row in result_set:
            response.message = response.message + "\n " + result_row[0].replace ("\\'", "'")
    else:
        response.message = "I could not find it"

def get_all_memories (user_id, response, cursor):
    query = "SELECT `fld_sentence`, `fld_timestamp` FROM `tbl_memories` WHERE `fld_user_id` = " + user_id + " ORDER BY `fld_timestamp`;"
    if cursor.execute (query) > 1:
        count = 1
        result_set = cursor.fetchall ()
        response.message = "I remember you told me"
        for result_row in result_set:
            response.message = response.message + "\n# " + str (count) + " " + result_row[0].replace ("\\'", "'")
            count = count + 1
    elif cursor.execute (query) == 1:
        result_set = cursor.fetchall ()
        response.message = "I remember you told me"
        for result_row in result_set:
            response.message = response.message + "\n " + result_row[0].replace ("\\'", "'")
    else:
        response.message = "I could not find anything"

def get_memories_to_delete (user_id, keywords, response, cursor):
    memory_id_list = []
    main_query = "SELECT `fld_id`, (0"
    sub_query = ""
    for word in keywords:
        sub_query = sub_query + " + (`fld_keywords` LIKE '%%%s%%')" % (word.replace ("'", "\\'"))
    main_query = main_query + sub_query + ") as global_hits FROM `tbl_memories` WHERE `fld_user_id` = " + user_id + " HAVING global_hits = (SELECT (0" + sub_query + ") as local_hits FROM `tbl_memories` HAVING local_hits > 0 ORDER BY local_hits DESC LIMIT 1) ORDER BY `fld_timestamp`;"
    if cursor.execute (main_query) > 0:
        result_set = cursor.fetchall ()
        for result_row in result_set:
            memory_id_list.append (result_row[0])
    return memory_id_list

def delete_memory (user_id, keywords, response, conn, cursor):
    memory_id_list = get_memories_to_delete (user_id, keywords, response, cursor)
    memory_id_str_list = ', '.join (str (memory_id) for memory_id in memory_id_list)
    if len (memory_id_list) > 0:
        query = "DELETE FROM `tbl_memories` WHERE `fld_id` IN (%s);" % memory_id_str_list
        try:
            cursor.execute (query)
            conn.commit ()
            response.message = "Done. It's forgotten"
        except:
            conn.rollback ()
            response.message = "Something went wrong, please try again"
    else:
        response.message = "I could not find it"

def delete_all_memories (user_id, response, conn, cursor):
    query = "SELECT `fld_id` FROM `tbl_memories` WHERE `fld_user_id` = %d;" % (user_id)
    if cursor.execute (query) > 0:
        query = "DELETE FROM `tbl_memories` WHERE `fld_user_id` = %d;" % (user_id)
        try:
            cursor.execute (query)
            conn.commit ()
            response.message = "Done. It's forgotten"
        except:
            conn.rollback ()
            response.message = "Something went wrong, please try again"
    else:
        response.message = "I could not find it"

def create_context (user_id, intent, conn, cursor):
    timestamp = time.time ()
    query = "INSERT INTO `tbl_contexts` (`fld_id`, `fld_user_id`, `fld_intent`, `fld_timestamp`) VALUES (%s, %s, '%s', %d)" % ('NULL', user_id, intent, timestamp)
    try:
        cursor.execute (query)
        conn.commit ()
        return (conn.insert_id () + 1)
    except:
        conn.rollback ()
        return 0

def delete_context (context_id, response, conn, cursor):
    query = "DELETE FROM `tbl_contexts` WHERE fld_id = %d" % (context_id)
    try:
        cursor.execute (query)
        conn.commit ()
        response.message = "Alright, it's cancelled"
    except:
        conn.rollback ()
        response.message = "Something went wrong, please try again"

def get_active_context (user_id, cursor):
    timestamp = time.time ()
    query = "SELECT `fld_id` FROM `tbl_contexts` WHERE (%f - `fld_timestamp`) < 120 AND `fld_user_id` = %s ORDER BY `fld_timestamp` DESC LIMIT 1" % (timestamp, user_id)
    if cursor.execute (query) == 1:
        result_set = cursor.fetchall ()
        return result_set[0][0]
    else:
        return 0

def get_context_intent (context_id, cursor):
    query = "SELECT `fld_intent` FROM `tbl_contexts` WHERE `fld_id` = %d" % (context_id)
    if cursor.execute (query) == 1:
        result_set = cursor.fetchall ()
        return result_set[0][0]
    else:
        return False

def create_slots (context_id, intent, entities, conn, cursor):
    if intent == "memories.get" or intent == "memories.create" or intent == "memories.delete":
        query = "INSERT INTO `tbl_slots` (`fld_id`, `fld_context_id`, `fld_slot_name`, `fld_slot_content`) VALUES (%s, %s, '%s', '%s')" % ('NULL', context_id, 'keyword', ' '.join (entities[0]['keyword']).replace ("'", "\\'"))
        try:
            cursor.execute (query)
            conn.commit ()
            return True
        except:
            conn.rollback ()
            return False

def get_all_slots (context_id, cursor):
    query = "SELECT `fld_slot_name`, `fld_slot_content` FROM `tbl_slots` WHERE `fld_id` = %d;" % (context_id)
    slots = []
    cursor.execute (query)
    result_set = cursor.fetchall ()
    for result_row in result_set:
        slots.append ({result_row[0]: result_row[1]})
    return slots

def fill_slot (context_id, slot_name, slot_content, conn, cursor):
    query = "UPDATE `tbl_slots` SET `fld_slot_content` = '%s' WHERE `fld_slot_name` = '%s' AND `fld_context_id` = %d" % (slot_content, slot_name, context_id)
    try:
        cursor.execute (query)
        conn.commit ()
        return True
    except:
        conn.rollback ()
        return False

def process_intent (user_id, sentence, intent, entities, response, conn, cursor):
    if intent == "memories.create":
        context_id = create_context (user_id, intent, conn, cursor)
        if create_slots (context_id, intent, entities, conn, cursor):
            if len (entities[0]['keyword']) > 0:
                create_memory (user_id, sentence, ' '.join (entities[0]['keyword']), response, conn, cursor)
            else:
                response.message = "What do you want me to remember?"
        else:
            response.message = "Something went wrong, please try again"
    elif intent == "memories.get":
        context_id = create_context (user_id, intent, conn, cursor)
        if create_slots (context_id, intent, entities, conn, cursor):
            if len (entities[0]['keyword']) > 0:
                get_memory (user_id, entities[0]['keyword'], response, cursor)
            else:
                response.message = "What are you looking for?"
        else:
            response.message = "Something went wrong, please try again"
    elif intent == "memories.get_all":
        get_all_memories (user_id, response, cursor)
    elif intent == "memories.delete":
        context_id = create_context (user_id, intent, conn, cursor)
        if create_slots (context_id, intent, entities, conn, cursor):
            if len (entities[0]['keyword']) > 0:
                delete_memory (user_id, entities[0]['keyword'], response, conn, cursor)
            else:
                response.message = "What do you want me to forget?"
        else:
            response.message = "Something went wrong, please try again"
    elif intent == "memories.delete_all":
        delete_all_memories (user_id, response, conn, cursor)
    elif intent == "greetings":
        response.message = "Hi, how can I help?"
    else:
        response.message = "I could not understand you"

@app.route('/user/login/')
def login ():
    response = Response ()
    conn = MySQLdb.connect (host = 'beinglabs.mysql.pythonanywhere-services.com', user = 'beinglabs', passwd = 'beingmailer2014', db = 'beinglabs$db_bighead')
    cursor = conn.cursor ()
    email = request.args ['email']
    password = request.args ['password']
    query = "SELECT `fld_email` FROM `tbl_users` WHERE `fld_email` = '" + email + "' AND `fld_password` = '" + password + "';"
    if cursor.execute (query) == 1:
        response.message = "success"
    else:
        response.message = "The login details you entered were incorrect"
    cursor.close ()
    conn.close ()
    return response.generate ()

@app.route('/user/register/')
def register ():
    response = Response ()
    conn = MySQLdb.connect (host = 'beinglabs.mysql.pythonanywhere-services.com', user = 'beinglabs', passwd = 'beingmailer2014', db = 'beinglabs$db_bighead')
    cursor = conn.cursor ()
    name = request.args ['name']
    email = request.args ['email']
    password = request.args ['password']
    query = "SELECT `fld_email` FROM `tbl_users` WHERE `fld_email` = '" + email + "';"
    if cursor.execute (query) == 0:
        query = "INSERT INTO `tbl_users` (`fld_id`, `fld_name`, `fld_email`, `fld_password`) VALUES (%s, '%s', '%s', '%s')" % ('NULL', name, email, password)
        try:
            cursor.execute (query)
            conn.commit ()
            response.message = "success"
        except:
            conn.rollback ()
            response.message = "Something went wrong while creating your account"
    else:
        response.message = "This e-mail ID is already registered"
    cursor.close ()
    conn.close ()
    return response.generate ()

@app.route('/')
def index ():
    response = Response ()
    conn = MySQLdb.connect (host = 'beinglabs.mysql.pythonanywhere-services.com', user = 'beinglabs', passwd = 'beingmailer2014', db = 'beinglabs$db_bighead')
    cursor = conn.cursor ()
    sentence = request.args ['sentence']
    user_id = request.args ['user_id']
    intent = ffc.classify (sentence)
    entities = ffner.recognize (sentence)
    response.intent = intent
    response.entities = entities
    fill_slot (1, 'keyword', 'book trunk', conn, cursor)
    return response.generate ()

@app.route('/main/')
def main ():
    response = Response ()
    conn = MySQLdb.connect (host = 'beinglabs.mysql.pythonanywhere-services.com', user = 'beinglabs', passwd = 'beingmailer2014', db = 'beinglabs$db_bighead')
    cursor = conn.cursor ()
    sentence = request.args ['sentence']
    user_id = request.args ['user_id']
    #query = "INSERT INTO `tbl_dump` (`fld_id`, `fld_sentence`) VALUES (%s, '%s')" % ('NULL', sentence.replace ("'", "\\'"))
    #cursor.execute (query)
    #conn.commit ()
    intent = ffc.classify (sentence)
    entities = ffner.recognize (sentence)

    response.intent = intent
    response.entities = entities

    active_context_id = get_active_context (user_id, cursor)
    if active_context_id == 0:
        process_intent (user_id, sentence, intent, entities, response, conn, cursor)
    else:
        context_intent = get_context_intent (active_context_id, cursor)
        slots = get_all_slots (active_context_id, cursor)
        if context_intent == "memories.create":
            if len (slots[0]['keyword']) > 0:
                if intent == "forget_that":
                    delete_memory (user_id, slots[0]['keyword'].split (), response, conn, cursor)
                else:
                    process_intent (user_id, sentence, intent, entities, response, conn, cursor)
            else:
                if len (entities[0]['keyword']) > 0:
                    if fill_slot (active_context_id, 'keyword', ' '.join (entities[0]['keyword']), conn, cursor):
                        create_memory (user_id, sentence, ' '.join (entities[0]['keyword']), response, conn, cursor)
                    else:
                        response.message = "Something went wrong, please try again"
                else:
                    if intent == "cancel":
                        delete_context (active_context_id, response, conn, cursor)
                    else:
                        response.message = "Try saying 'Remember that my book is in trunk'"
        elif context_intent == "memories.get":
            if len (slots[0]['keyword']) > 0:
                if intent == "forget_that":
                    delete_memory (user_id, slots[0]['keyword'].split (), response, conn, cursor)
                else:
                    process_intent (user_id, sentence, intent, entities, response, conn, cursor)
            else:
                if len (entities[0]['keyword']) > 0:
                    if fill_slot (active_context_id, 'keyword', ' '.join (entities[0]['keyword']), conn, cursor):
                        get_memory (user_id, entities[0]['keyword'], response, cursor)
                    else:
                        response.message = "Something went wrong, please try again"
                else:
                    if intent == "cancel":
                        delete_context (active_context_id, response, conn, cursor)
                    else:
                        response.message = "Try saying 'Where is my book?'"
        elif context_intent == "memories.delete":
            if len (slots[0]['keyword']) > 0:
                    process_intent (user_id, sentence, intent, entities, response, conn, cursor)
            else:
                if len (entities[0]['keyword']) > 0:
                    if fill_slot (active_context_id, 'keyword', ' '.join (entities[0]['keyword']), conn, cursor):
                        delete_memory (user_id, entities[0]['keyword'], response, conn, cursor)
                    else:
                        response.message = "Something went wrong, please try again ID"
                else:
                    if intent == "cancel":
                        delete_context (active_context_id, response, conn, cursor)
                    else:
                        response.message = "Try saying 'Forget what I said about my book?'"
    cursor.close ()
    conn.close ()
    return response.generate ()
