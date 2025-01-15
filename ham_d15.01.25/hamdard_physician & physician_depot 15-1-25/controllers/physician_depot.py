                   
#==============================  ADD PHYSICIAN DEPOT FUNCTION  ====================================#

def physician_depot_add():  

    # if ((session.cid==None) or (session.cid=='None')):
    #     redirect(URL('default','index'))
    response.title='Physician Depot Add'
    submit=request.vars.submit
    c_id=session.cid
    # return c_id
    search_value=str(request.vars.searchValue_OpName).strip().replace('None','')
    session.search_value = search_value
    filter_button = str(request.vars.btn_filter).strip()
    all_button = str(request.vars.btn_all).strip()
    depot_id = str(request.vars.depot_id).strip()
    depot_id1=str(request.vars.depot_id1).strip()
    session.depot_id1 = depot_id1
    physician_condition=''

    if submit == 'Save':

        physician_id = str(request.vars.physician_id).split('|')[0]
        physician_name= str(request.vars.physician_id).split('|')[1]
        
        depot_id= str(request.vars.depot_id).split('|')[0]
        depot_name= str(request.vars.depot_id).split('|')[1]
        # physician_password = request.vars.physician_password
        # return physician_name, depot_name, physician_id, depot_id
        if physician_id!='' or depot_id!='':
            check_physician_sql = "select physician_id, depot_id from sm_physician_depot where cid = '"+c_id+"' and  physician_id='"+str(physician_id)+"' and depot_id = '"+str(depot_id)+"';"
            # return check_physician_sql
            checkphysicianRows = db.executesql(check_physician_sql, as_dict=True)
            if len(checkphysicianRows) > 0:
                response.flash = 'Physician ID and Depot ID already exists'
               
            else:
                check_depot_id_sql = "select depot_id from sm_depot where depot_id='"+str(depot_id)+"'"
                # return check_depot_id_sql
                check_depot_id = db.executesql(check_depot_id_sql, as_dict=True)

                if len(check_depot_id) > 0:
                    insertphysician_sql = "INSERT INTO sm_physician_depot (cid, physician_id, physician_name, depot_id, depot_name) VALUES ('"+str(c_id)+"','"+str(physician_id)+"', '"+str(physician_name)+"', '"+str(depot_id)+"', '"+str(depot_name)+"')"      
                    # return insertphysician_sql
                    insertphysician = db.executesql(insertphysician_sql)
                    response.flash= 'Physician Depot Insert Successfully'
                else:
                    response.flash= 'Depot User Does not exits'

    
    if filter_button == "Filter":
        if session.search_value!='':
            physician_id = session.search_value.split('|')[0].upper()
            session.physician_id=session.search_value
            physician_condition = physician_condition+" and physician_id = '"+str(physician_id)+"' "
            # physicianRows_sql = "SELECT physician_id, physician_name from sm_physician where cid = '"+c_id+"' and  physician_name='"+str(search_value)+"' order by physician_id;"

        if session.depot_id1!='':
            physician_condition = physician_condition+ " and depot_id = '"+str(session.depot_id1)+"'"
            # return physician_condition
    if all_button == "All":
        physician_condition = ""
        session.filter_button = None
        session.search_value = ""
        session.physician_id = ""
        session.depot_id1=""

    physicianRows_sql = "SELECT physician_id, physician_name, depot_id, depot_name from sm_physician_depot where cid = '"+c_id+"' "+ physician_condition+" order by depot_id;"
    physicianRows = db.executesql(physicianRows_sql, as_dict=True)

    session.physician_condition = physician_condition
    return dict(physicianRows=physicianRows)



#============================== PHYSICIAN DEPOT AUTO COMPLETE FUNCTION  ====================================#

         
def physician_depot_list():
    c_id = session.cid
    retStr = ''

    userRows_sql = "select physician_id, physician_name from sm_physician where cid = '"+c_id+"' order by physician_id;"
    userRows = db.executesql(userRows_sql, as_dict=True)
    for i in range(len(userRows)):
        records_ov_dict=userRows[i]   
        physician_id=str(records_ov_dict["physician_id"])
        physician_name=str(records_ov_dict["physician_name"])
        if retStr == '':
            retStr = physician_id +'|'+ physician_name
        else:
            retStr += ',' +physician_id +'|'+ physician_name
    
    return retStr


#============================== DEPOT ID AUTO COMPLETE FUNCTION  ====================================#


def depot_list():
    c_id = session.cid
    retStr = ''

    userRows_sql = "select depot_id, name from sm_depot where cid = '"+c_id+"' order by depot_id;"
    userRows = db.executesql(userRows_sql, as_dict=True)
    for i in range(len(userRows)):
        records_ov_dict=userRows[i]   
        depot_id=str(records_ov_dict["depot_id"])
        depot_name=str(records_ov_dict["name"])
        if retStr == '':
            retStr = depot_id +'|'+ depot_name
        else:
            retStr += ',' +depot_id +'|'+ depot_name
    
    return retStr                                 


#============================== PHYSICIAN ID AUTO COMPLETE FUNCTION  ====================================#


def physician_id_list():
    c_id = session.cid
    retStr = ''

    userRows_sql = "select physician_id from sm_physician where cid = '"+c_id+"' order by physician_id;"
    userRows = db.executesql(userRows_sql, as_dict=True)
    for i in range(len(userRows)):
        records_ov_dict=userRows[i]   
        physician_id=str(records_ov_dict["physician_id"])
        # physician_name=str(records_ov_dict["physician_name"])
        if retStr == '':
            retStr = physician_id
        else:
            retStr += ',' +physician_id
    
    return retStr



#============================== PHYSICIAN DEPOT DELETE FUNCTION  ====================================#


def physician_depot_delete():
    c_id = session.cid
    physician_id = request.args(0)
    # return physician_id
    btn_delete = request.vars.btn_delete
    delete_sql = "delete from sm_physician_depot where cid = '"+c_id+"' and physician_id='"+str(physician_id)+"' "
    records = db.executesql(delete_sql)
    session.flash = 'Deleted Successfully'
    redirect (URL('physician_depot','physician_depot_add'))



#============================== PHYSICIAN DEPOT UPDATED FUNCTION ====================================#


def physician_depot_edit():
    c_id = session.cid
    physician_id = request.args(0)
    physician_name = request.args(1)
    depot_id = request.args(2)
    depot_name = request.args(3)
    # physician_mobile = request.args(2)
    # physician_password = request.args(3)
    
    btn_delete = request.vars.btn_delete
    update_btn=request.vars.update_btn

    if update_btn:
        physician_ID = request.args(0)
        # return physician_ID
        
        physician_id = str(request.vars.physician_id).split('|')[0]
        physician_name= str(request.vars.physician_id).split('|')[1]
        
        depot_id= str(request.vars.depot_id).split('|')[0]
        depot_name= str(request.vars.depot_id).split('|')[1]
        # physician_mobile = str(request.vars.physician_mobile).strip()
        # physician_password = str(request.vars.physician_password).strip()
        update_physician_sql= " Update sm_physician_depot Set physician_id= '"+str(physician_id)+"', physician_name= '"+str(physician_name)+"', depot_id= '"+str(depot_id)+"' , depot_name= '"+str(depot_name)+"' where cid = '"+c_id+"' and  physician_id ='"+str(physician_ID)+"'"  
        # return update_physician_sql
        update_physician = db.executesql(update_physician_sql)
        session.flash = 'Physician Depot Updated Successfully'
        redirect(URL('physician_depot','physician_depot_add'))

    if btn_delete:
        physician_ID = request.args(0)
        delete_sql = "delete from sm_physician_depot where cid = '"+c_id+"' and physician_id='"+str(physician_id)+"' "
        records = db.executesql(delete_sql)
        session.flash = 'Deleted Successfully'
        redirect (URL('physician_depot','physician_depot_add'))

    
    return dict(physician_id= physician_id, physician_name=physician_name,  depot_id = depot_id, depot_name= depot_name)






#============================== PHYSICIAN DEPOT LIST DOWNLOAD FUNCTION ====================================#

def physician_depot_list_Download():
    c_id = session.cid
    physicianRows_sql = "SELECT physician_id,physician_name, depot_id, depot_name from sm_physician_depot where cid = '"+c_id+"' '"+ session.physician_condition+"' order by physician_id;"
    physicianRows = db.executesql(physicianRows_sql, as_dict=True)
    # return record
    myString = 'Physician Depot List\n\n'
    myString += 'Physician ID, Physician Name, Depot ID, Depot Name\n'
    total=0
    attTime = ''
    totalCount = 0
    for i in range(len(physicianRows)):
        recordsStr = physicianRows[i]
        physician_id = str(recordsStr['physician_id'])
        physician_name = str(recordsStr['physician_name']).replace('None', '')
        depot_id = str(recordsStr['depot_id'])
        depot_name = str(recordsStr['depot_name']).replace('None', '')
       
        
        myString += str(physician_id) + ','+str(physician_name) + ',' + str(depot_id) +',' + str(depot_name) + ',\n'

    # Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_physician_depot.csv'
    return str(myString)



#============================== PHYSICIAN DEPOT BATCH UPLOAD FUNCTION ====================================#

def physician_depot_batch_upload():
   
    response.title = 'Physician Depot Batch Upload'
    cid=session.cid
    btn_upload=request.vars.btn_upload
    # depot_id = str(request.vars.depot_id).strip()
    # return depot_id
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
        # for i in range(total_row):
        #     if i>=100:
        #         break
        #     else:
        #         row_data=row_list[i]                    
        #         coloum_list=row_data.split( '\t')
        #         if len(coloum_list)==2:
        #             ffExcel=str(coloum_list[0]).strip().upper()
                    
        #             if ffExcel!='':
        #                 if ffExcel not in ff_list_excel:ff_list_excel
        #                 ff_list_excel.append(ffExcel)       

        for i in range(total_row):
            if i>=500:
                break
            else:
                row_data=row_list[i]
                coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)!=2:
                error_data=row_data+'(2 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
            else:
                physician_idExcel = str(coloum_list[0]).strip().upper()
                # return physician_idExcel
                depot_idExcel = str(coloum_list[1]).strip().upper()              
                    
                if physician_idExcel==''or physician_idExcel == 'NONE' or physician_idExcel=='' or physician_idExcel== 'NONE' or depot_idExcel=='' or depot_idExcel == 'NONE':
                    error_data=row_data+'(Required all value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue                    
                
                else:
                    
                    existCheckPhysicianRows= " select * FROM sm_physician WHERE cid='"+str(cid)+"' and physician_id = '"+str(physician_idExcel)+"' LIMIT 0,1"
                    # return existCheckRows
                    existCheckPhysician = db.executesql(existCheckPhysicianRows)

                    if len(existCheckPhysician) == 0:
                        error_data=row_data+'(Physician does not exits)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue

                    else:
                        check_depot_id_sql = "select depot_id from sm_depot where  cid='"+str(cid)+"' and depot_id='"+str(depot_idExcel)+"' LIMIT 0,1"
                        # return check_depot_id_sql
                        check_depot_id = db.executesql(check_depot_id_sql, as_dict=True)

                        if len(check_depot_id) == 0:
                            response.flash= 'Depot User Does not exits'
                            error_data=row_data+'(Depot User Does not exits)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            existCheckRowsDuplicate_sql= "select physician_id, depot_id FROM sm_physician_depot WHERE cid='"+str(cid)+"' and physician_id = '"+str(physician_idExcel)+"' and depot_id = '"+str(depot_idExcel)+"' LIMIT 0,1"
                            # return existCheckRows
                            existCheckRowsDuplicate = db.executesql(existCheckRowsDuplicate_sql)

                            if len(existCheckRowsDuplicate) > 0:
                                error_data=row_data+'(Duplicate Physician ID and Depot ID)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue

                            else:
                                physician_name_sql = f"select physician_name from sm_physician where cid='"+str(cid)+"' and physician_id = '"+str(physician_idExcel)+"';"
                                physician_name = db.executesql(physician_name_sql, as_dict=True)[0]['physician_name']
                                
                                depot_name_sql = f"select name from sm_depot where cid='"+str(cid)+"' and depot_id = '"+str(depot_idExcel)+"';"
                                depot_name = db.executesql(depot_name_sql, as_dict=True)[0]['name']
                                
                                try:
                                    insert_physician_depot_sql = "INSERT INTO sm_physician_depot (cid, physician_id, physician_name, depot_id, depot_name) VALUES ('"+str(cid)+"','"+str(physician_idExcel)+"', '"+str(physician_name)+"','"+str(depot_idExcel)+"' ,'"+str(depot_name)+"');"
                                    # return insert_physician_depot_sql
                                    insert_physician_depot = db.executesql(insert_physician_depot_sql)
                                    count_inserted+=1
                                except Exception as e:
                                    error_str = 'Please do not insert special charachter.'
        if error_str=='':
            error_str='No error'

    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)