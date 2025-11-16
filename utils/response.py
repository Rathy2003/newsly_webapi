def success_response(data, message="Success", status_code=200):
    return {"message": message,"status":status_code,"data": data}