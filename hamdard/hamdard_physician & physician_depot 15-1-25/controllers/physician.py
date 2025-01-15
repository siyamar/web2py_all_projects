                   
                    #### ADD PHYSICIAN ######

def physician_add():  

    # if ((session.cid==None) or (session.cid=='None')):
    #     redirect(URL('default','index'))
    response.title='physician Add'
    submit=request.vars.submit
    c_id=session.cid
    search_value=str(request.vars.searchValue_OpName).strip().replace('None','')
    session.search_value = search_value
    search_value_opGender=str(request.vars.searchValue_OpGender).strip().replace('None','')
    session.search_value_opGender = search_value_opGender
    filter_button = str(request.vars.btn_filter).strip()
    all_button = str(request.vars.btn_all).strip()
    physician_condition=''

    if submit:
        physician_id = str(request.vars.physician_id)
        physician_name= str(request.vars.physician_name).split(',')[0]
        physician_mobile = request.vars.physician_mobile
        gender = request.vars.gender
        # physician_password = request.vars.physician_password
        # return physician_name
        if physician_id!='' and physician_name!='':
            check_physician_sql = "select physician_id, physician_name from sm_physician where cid = '"+c_id+"' and  physician_id='"+str(physician_id)+"' and physician_name = '"+str(physician_name)+"';"
            # return check_physician_sql
            checkphysicianRows = db.executesql(check_physician_sql, as_dict=True)
            if len(checkphysicianRows) > 0:
                response.flash = 'Physician already exists'
               
            else:
                insertphysician_sql = "INSERT INTO sm_physician (cid, physician_id, physician_name, mobile_no, gender) VALUES ('"+str(c_id)+"','"+str(physician_id)+"','"+str(physician_name)+"','"+str(physician_mobile)+"', '"+str(gender)+"')"      
                # return insertphysician_sql
                insertphysician = db.executesql(insertphysician_sql)
                response.flash= 'Physician Insert Successfully'
    
    if filter_button == "Filter":
        if session.search_value!='':
            physician_id = session.search_value.split('|')[0].upper()
            session.physician_name=session.search_value
            physician_condition = physician_condition+" and physician_id = '"+str(physician_id)+"' "
            # physicianRows_sql = "SELECT physician_id, physician_name from sm_physician where cid = '"+c_id+"' and  physician_name='"+str(search_value)+"' order by physician_id;"

        if session.search_value_opGender != '':
            gender = session.search_value_opGender
            physician_condition = physician_condition+ " and gender = '"+str(gender)+"' "
            
    if all_button == "All":
        physician_condition = ""
        session.filter_button = None
        session.search_value = ""
        session.physician_name = ""

    physicianRows_sql = "SELECT physician_id, physician_name, mobile_no, gender, password from sm_physician where cid = '"+c_id+"' "+ physician_condition+" order by physician_id;"
    physicianRows = db.executesql(physicianRows_sql, as_dict=True)

    session.physician_condition = physician_condition
    return dict(physicianRows=physicianRows)


         
def physician_list():
    c_id = session.cid
    retStr = ''

    userRows_sql = "select physician_id, physician_name from sm_physician where cid = '"+c_id+"' order by physician_id;"
    userRows = db.executesql(userRows_sql, as_dict=True)
    for i in range(len(userRows)):
        records_ov_dict=userRows[i]   
        physician_id=str(records_ov_dict["physician_id"])
        physician_name=str(records_ov_dict["physician_name"])
        if retStr == '':
            retStr = physician_id+'|'+physician_name
        else:
            retStr += ',' +physician_id+'|'+physician_name
    
    return retStr



def physician_delete():
    c_id = session.cid
    physician_id = request.args(0)
    # return physician_id
    btn_delete = request.vars.btn_delete
    delete_sql = "delete from sm_physician where cid = '"+c_id+"' and physician_id='"+str(physician_id)+"' "
    records = db.executesql(delete_sql)
    session.flash = 'Deleted Successfully'
    redirect (URL('physician','physician_add'))



def physician_edit():
    c_id = session.cid
    physician_id = request.args(0)
    physician_name = request.args(1)
    physician_mobile = request.args(2)
    gender = request.args(3)
    physician_password = request.args(4)
    
    btn_delete = request.vars.btn_delete
    update_btn=request.vars.update_btn

    if update_btn:
        physician_ID = request.args(0)
        # return physician_ID
        physician_id = str(request.vars.physician_id).strip()
        physician_name = str(request.vars.physician_name).strip()
        physician_mobile = str(request.vars.physician_mobile).strip()
        gender = str(request.vars.gender).strip()
        physician_password = str(request.vars.physician_password).strip()
        update_physician_sql= " Update sm_physician Set physician_id= '"+str(physician_id)+"', physician_name= '"+str(physician_name)+"', mobile_no= '"+str(physician_mobile)+"',gender= '"+str(gender)+"', password= '"+str(physician_password)+"' where cid = '"+c_id+"' and  physician_id ='"+str(physician_ID)+"' "  
        # return update_physician_sql
        update_physician = db.executesql(update_physician_sql)
        session.flash = 'Physician Updated Successfully'
        redirect(URL('physician','physician_add'))

    if btn_delete:
        physician_ID = request.args(0)
        delete_sql = "delete from sm_physician where cid = '"+c_id+"' and physician_id='"+str(physician_id)+"' "
        records = db.executesql(delete_sql)
        session.flash = 'Deleted Successfully'
        redirect (URL('physician','physician_add'))

    
    return dict(physician_id= physician_id, physician_name = physician_name, physician_mobile= physician_mobile,gender=gender, physician_password = physician_password)






                    #### PHYSICIAN LIST DOWNLOAD ######

def physician_list_Download():
    c_id = session.cid
    physicianRows_sql = "SELECT physician_id, physician_name, mobile_no, gender,  password from sm_physician where cid = '"+c_id+"' "+ session.physician_condition+" order by physician_id;"
    physicianRows = db.executesql(physicianRows_sql, as_dict=True)
    # return record
    myString = 'Physician List\n\n'
    myString += 'Physician ID, Physician Name, Mobile No, Gender, Password\n'
    total=0
    attTime = ''
    totalCount = 0
    for i in range(len(physicianRows)):
        recordsStr = physicianRows[i]
        physician_id = str(recordsStr['physician_id'])
        physician_name = str(recordsStr['physician_name'])
        physician_mobile = str(recordsStr['mobile_no'])
        gender = str(recordsStr['gender']).replace("None", "")
        physician_password = str(recordsStr['password'])
        
        myString += str(physician_id) + ',' + str(physician_name) + ',' + str(physician_mobile) + ',' + str(gender) + ',' + str(physician_password) + ',\n'

    # Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_physician.csv'
    return str(myString)



            ######################## PHYSICIAN BATCH UPLOAD ######################

def physician_batch_upload():
   
    response.title = 'Physician Batch Upload'
    cid=session.cid
    btn_upload=request.vars.btn_upload
    count_inserted=0
    count_error=0
    error_str=''
    total_row=0
            
    if btn_upload=='Upload':
        excel_data=str(request.vars.excel_data)
        inserted_count=0
        error_count=0
        
        row_list=excel_data.split( '\n')
        total_row=len(row_list)
        
        ff_list_exist=[]   
        ff_list_excel=[]
                
        ins_list=[]
        ins_dict={}

        # ----------------------
        for i in range(total_row):
            if i>=100:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==4:
                    ffExcel=str(coloum_list[0]).strip().upper()
                    
                    if ffExcel!='':
                        if ffExcel not in ff_list_excel:ff_list_excel
                        ff_list_excel.append(ffExcel)       

        for i in range(total_row):
            if i>=100:
                break
            else:
                row_data=row_list[i]
                coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)!=5:
                error_data=row_data+'(5 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
            else:
                employee_idExcel = str(coloum_list[0]).strip().upper()
                # return employee_idExcel
                employee_nameExcel = str(coloum_list[1]).strip().upper()
                employee_mobileExcel = str(coloum_list[2]).strip().upper()               
                employee_genderExcel = str(coloum_list[3]).strip().upper()               
                employee_passwordExcel = str(coloum_list[4]).strip().upper()               
                    
                if employee_idExcel==''or employee_idExcel == 'NONE' or employee_idExcel=='' or employee_idExcel== 'NONE' or employee_nameExcel=='' or employee_nameExcel == 'NONE':
                    error_data=row_data+'(Required all value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue                    
                
                else:
                    existCheckRows= " select * FROM sm_physician WHERE cid='"+str(cid)+"' and physician_id = '"+str(employee_idExcel)+"' LIMIT 0,1"
                    # return existCheckRows
                    existCheck = db.executesql(existCheckRows)

                    if len(existCheck) > 0:
                        error_data=row_data+'(Duplicate Physician check)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        try:
                            insert_sql = "INSERT INTO sm_physician (cid, physician_id, physician_name, mobile_no,gender, password) VALUES ('"+str(cid)+"','"+str(employee_idExcel)+"','"+str(employee_nameExcel)+"', '"+str(employee_mobileExcel)+"', '"+str(employee_genderExcel)+"','"+str(employee_passwordExcel)+"');"
                            # return insert_sql
                            update_ff_list = db.executesql(insert_sql)
                            count_inserted+=1
                        except Exception as e:
                            error_str = 'Please do not insert special charachter.'
                                
        if error_str=='':
            error_str='No error'

    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)