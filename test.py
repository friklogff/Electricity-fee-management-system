import base64
import jwt
itoken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NjExNzg2NCwianRpIjoiZGRhODRjM2YtNTkxMS00MTg4LTk5ZGEtZWRjNDI0NzRmYWIwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjg2MTE3ODY0LCJleHAiOjE2ODYxMTk2NjQsInByaXZpbGVnZSI6MX0.-GSErFaPb_bm3Qmh-Rlr7vJBpb40KJCV4kE8d2mx2fo"


claims = jwt.decode(itoken, 'secret', algorithms=['HS256'])
print(claims)
#
# def parse_token(token):
#     try:
#         payload = token.split('.')[1]
#         payload_data = base64.b64decode(payload, validate=True)
#         claims = payload_data.decode('utf-8')
#
#         role = claims.split(',')[1]
#         return role
#     except Exception as e:
#         return {'errmsg': 'Invalid token'}
#
#
# role = parse_token(token)
# print(role)  # admin
#
