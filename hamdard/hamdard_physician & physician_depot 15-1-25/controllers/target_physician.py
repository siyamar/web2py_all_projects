from datetime import datetime
def target_physician():
    submit = request.vars.submit
    branch_id_filter = request.vars.branch_id_filter
    gender_filter = request.vars.gender_filter
    first_date_filter = request.vars.first_date_filter
    btn_filter = request.vars.btn_filter
    btn_all = request.vars.btn_all
    cid = session.cid
    condition = ''
    reqPage = len(request.args)
    
# ===========post operation ==========
    
    if submit:
        branch_id = request.vars.branch_id
        branch_name = branch_id.split('|')[1]
        gender = request.vars.gender
        target = request.vars.target
        first_date = request.vars.first_date
        
        
        if branch_id == "" or branch_id == "None" or branch_id == None:
           session.flash="Required Branch ID"
        #    return "Required Branch ID" 
       
        elif branch_id != "" or branch_id != "None" or branch_id != None:
            branch_id = branch_id.split("|")[0]
            branch_id_check = "select * from sm_depot where depot_id = '"+str(branch_id)+"'"
            branch_id_check_result = db.executesql(branch_id_check, as_dict=True)
            
            if len(branch_id_check_result) == 0:
                session.flash= "Invalid Branch ID"
    
            elif gender == "" or gender == "None"or gender == None:
            # response.flash = "Required gender"
                session.flash= "Required gender"
            elif target == "" or target == "None" or target ==None:
            # response.flash = "Required target"
                session.flash= "Required target"
            elif first_date == "" or first_date == "None" or first_date == None:
            # response.flash = "Required first date"
                session.flash= "Required First date"
        
            elif first_date != "" or first_date != "None" or first_date != None:
                duplicate_month_check_sql = "SELECT count(id) as total FROM target_physician WHERE branch_id = '"+str(branch_id)+"' AND YEAR(first_date) = YEAR('"+str(first_date)+"') AND MONTH(first_date) = MONTH('"+str(first_date)+"') AND gender = ('"+str(gender)+"');"
                # return duplicate_month_check
            
                duplicate_month_check_result = db.executesql(duplicate_month_check_sql, as_dict = True)
                duplicate_month_check_res = duplicate_month_check_result[0]['total']
                if duplicate_month_check_res > 0:
                    session.flash="Duplicate Entry!"
        
                else:
                    insert_target_physician_sql = f"INSERT INTO target_physician (cid, branch_id, branch_name, gender, target, first_date) VALUES('{cid}', '{branch_id}', '{branch_name}', '{gender}', '{target}', '{first_date}')"
                    # return insert_target_physician_sql
                    insert_target_physician = db.executesql(insert_target_physician_sql)
        redirect(URL(c='target_physician',f='target_physician'))
    
    # --------paging
    session.items_per_page = 10
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = session.items_per_page
    limitby = f"{page * items_per_page}, {(page + 1) * items_per_page + 1}"
    # return limitby
    
# =============Filter=============
    if btn_filter == "Filter":
        if branch_id_filter !="" :
            branch_id_filter = branch_id_filter.split("|")[0]
            condition = condition + f"and branch_id='{branch_id_filter}'"  
            session.condition = condition
        if gender_filter !="" :
            condition = condition + f"and gender = '{gender_filter}'"
            session.condition = condition
        if first_date_filter !="" :  
            condition = condition + f"and first_date = '{first_date_filter}'"
            session.condition = condition
         
    if btn_all == "All":
        condition = ""
        session.condition = condition
# ===========get operation ==========
    rows_sql = "SELECT * FROM target_physician where cid = '"+str(cid)+"'"+condition+" order by id DESC LIMIt "+limitby+";"
    rows = db.executesql(rows_sql, as_dict=True)
    
# ===========total rows ============
    total_rows_sql = "SELECT COUNT(id) as total FROM target_physician  where cid = '"+str(cid)+"' "+condition+" order by id DESC;"
    total_rows = db.executesql(total_rows_sql, as_dict=True)
    total_rec = total_rows[0]['total']
    
    return dict(page=page, items_per_page= items_per_page, rows = rows, total_rec = total_rec)

# ===========Edit============
def target_physician_edit():
    row_id = request.args(0)
    update_btn= request.vars.update_btn
    delete_btn = request.vars.delete_btn
    
    select_target_physician_row_sql = f"select * from target_physician where id = '{row_id}';"
    select_target_physician_row = db.executesql(select_target_physician_row_sql, as_dict=True)
    
    for i in range(len (select_target_physician_row)):
        target_physician_row = select_target_physician_row[i]
        branch_id = str(target_physician_row['branch_id'])
        gender = str(target_physician_row['gender'])
        target = str(target_physician_row['target'])
        first_date = str(target_physician_row['first_date'])
        
    if update_btn:
        gender_up = request.vars.gender
        target_up = request.vars.target
        first_date_up = request.vars.first_date
        # return gender_up, target_up, first_date_up
        
        update_sql = f"UPDATE target_physician SET gender = '{gender_up}', target = '{target_up}', first_date = '{first_date_up}' where id = '{row_id}';"
        # return update_sql
        update = db.executesql(update_sql)
        # return 10
        
        redirect (URL('target_physician','target_physician' ))
    
    if delete_btn:
        delete_sql = f"DELETE FROM target_physician WHERE id = '{row_id}'"
        delete = db.executesql(delete_sql)
        
        redirect(URL('target_physician', 'target_physician'))
    
    return dict(row_id =row_id , branch_id=branch_id, gender=gender, target=target, first_date=first_date)

# ============auto complete==========

def get_branch_id_list():
    resStr = ''
    resStrdate = ''
    
    target_physician_list_rows_sql = "select * from target_physician;"
    target_physician_list_rows = db.executesql(target_physician_list_rows_sql, as_dict = True)
    
    for i in range(len(target_physician_list_rows)):
        target_physician_list_dict = target_physician_list_rows[i]
        
        branch_id = str(target_physician_list_dict['branch_id'])
        first_date = str(target_physician_list_dict['first_date'])
        
        if resStr == '':
            resStr = branch_id
        else:
            resStr += "," + branch_id
            
        if resStrdate == '':
            resStrdate = first_date
        else:
            resStrdate += "," + first_date
    return resStr

# ============auto complete for  Branch id from sm_depot==========

def get_branch_id_list_sm_depot():
    resStr = ''
    
    target_physician_list_rows_sql = "select * from sm_depot;"
    target_physician_list_rows = db.executesql(target_physician_list_rows_sql, as_dict = True)
    
    for i in range(len(target_physician_list_rows)):
        target_physician_list_dict = target_physician_list_rows[i]
        
        branch_id = str(target_physician_list_dict['depot_id'])
        branch_name = str(target_physician_list_dict['name'])
        
        if resStr == '':
            resStr = branch_id + '|' + branch_name
        else:
            resStr += "," + branch_id + '|' + branch_name
    return resStr

# ============auto complete for first date==========

def get_first_date_list():
    resStr = ''
    
    target_physician_list_rows_sql = "select distinct first_date from target_physician;"
    target_physician_list_rows = db.executesql(target_physician_list_rows_sql, as_dict = True)
    
    for i in range(len(target_physician_list_rows)):
        target_physician_list_dict = target_physician_list_rows[i]
        
        first_date = str(target_physician_list_dict['first_date'])
        
        if resStr == '':
            resStr = first_date
        else:
            resStr += "," + first_date
    return resStr
# ===========Download==========
def target_physician_download():
    cid = 'HAMDARD'
    condition = ''
    condition = session.condition
    # return condition
    download_sql = f"SELECT * FROM target_physician WHERE cid = '{cid} '{condition};"
    download_records = db.executesql(download_sql, as_dict = True)
    # return download_sql
    
    myString = 'Target Physician \n\n'
    myString += 'Branch Id, Gender, Target, First Date\n'
    
    for i in range(len(download_records)):
        download_dict = download_records[i]
        branch_id = str(download_dict['branch_id'])
        gender = str(download_dict['gender'])
        target = str(download_dict['target'])
        first_date = str(download_dict['first_date'])
        
        myString += str(branch_id) + ', ' + str(gender) + ', ' + str(target) +', ' + str(first_date)+ '\n'
        
# ============save as csv==========
    import gluon.contenttype
    response.headers['Content-Type'] =gluon.contenttype.contenttype('.csv')
    response.headers['Content_Disposition'] = 'attachment ; filename = download_target_physician.csv'
    return str(myString)

# ============batch upload============
def target_physician_batch_upload():
    cid = 'HAMDARD'
    btn_upload = request.vars.btn_upload
    count_error = 0
    count_inserted = 0
    error_str = ''
    total_row = 0
    
    if btn_upload == "Upload":
        excel_data = str(request.vars.excel_data)
        row_list = excel_data.split('\n')
        total_row = len(row_list)
        # return total_row
        
        for i in range(total_row):
            if i>= 500:
                break
            else:
                row_data =row_list[i]
                column_list = row_data.split('\t')
                
            if len (column_list) != 4:
                error_data = row_data + '(4 columns need in a row)\n'
                error_str = error_str + error_data
                    # return error_str
                count_error += 1
                continue
            else:
                branch_id_excel = str(column_list[0]).strip()
                gender_excel = str(column_list[1]).strip()
                target_excel = str(column_list[2]).strip()
                first_date_excel = str(column_list[3]).strip()
                branch_name=''
                branch_name_record_sql= f"select name from sm_depot where depot_id = '{branch_id_excel}'"
                # return branch_name_sql
                branch_name_record = db.executesql(branch_name_record_sql, as_dict=True)[0]
                if branch_name_record:
                    branch_name = branch_name_record['name']
                # return branch_name
                    
                if (branch_id_excel == "" or branch_id_excel == "None") and (gender_excel == "" or gender_excel=="None") and (target_excel == "" or target_excel=="None") and (first_date_excel =="" or first_date_excel == "None"):
                    error_data = row_data + '(Required All Field Value)\n'
                    error_str = error_str + error_data
                    count_error += 1
                    continue
                else:

                    existCheckRows = f"Select * from target_physician where branch_id = '{branch_id_excel}' AND YEAR(first_date) = YEAR('{first_date_excel}') AND MONTH(first_date) = MONTH('{first_date_excel}') AND gender = '{gender_excel}';"
                    existCheck = db.executesql(existCheckRows, as_dict=True)
                        # return existCheckRows
                    if len(existCheck) > 0:
                        # return "Double"
                        error_data = row_data + '(In this month "'+(gender_excel)+'" record already exist)\n'
                        error_str = error_str + error_data
                        count_error += 1
                        continue
                        
                    else:
                        try:
                            insert_sql = f"insert into target_physician (cid, branch_id, branch_name, gender, target, first_date) VALUES ('{cid}', '{branch_id_excel}', '{branch_name}','{gender_excel}', '{target_excel}', '{first_date_excel}');"
                            # return insert_sql
                            
                            insert = db.executesql(insert_sql)
                            count_inserted += 1
                        except Exception as e:
                            error_str = 'Please do not insert special charachter.'
                            
        if error_str == '':
            error_str = 'No Error'               

    return dict (count_error= count_error, count_inserted=count_inserted, error_str= error_str, total_row=total_row)
