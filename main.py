import aiohttp
import asyncio
import config
import processData as pd
import sys
import random as rd
import json

async def fetchData(url, callback = pd.processData, params=None):
    #set request url and parameters here or you can pass from outside. 
    
    #use s.** request a webside will keep-alive the connection automaticaly,
    #so you can set multi request here without close the connection 
    #while in the same domain.
    #i.e. 
    #await s.get('***/page1')
    #await s.get('***/page2')
    ########################################################################            
    headers=config.HEADERS    
    code='abcdefghijklmnopqrstuvwxyz0123456789'

    params={
        'poll[]':'8'
    }
    succeed=0
    n=0
    f = open('succeed.txt','w', encoding='utf-8')

    while True:       
        uid=''
        for i in range(26):
            uid+=code[rd.randint(0,35)] 
        # print(uid)

        headers['Cookie']='PHPSESSID='+uid+';'
        conn = aiohttp.TCPConnector(limit=config.REQ_AMOUNTS)    
        s = aiohttp.ClientSession(headers = config.HEADERS, connector=conn)
        
        async with s.post(url, params = params) as r:    
            #here the conection closed automaticly.            
            r= await r.text(encoding='utf-8')
            n+=1
            if n%1000 ==0:                
                with open('respone.txt','w', encoding='utf-8') as ff:
                    ff.write(r)
            r=json.loads(r)
            if r['status'] == 1:
                succeed+=1            
                f.write(str(succeed)+'\n')
                f.flush()            
                
            # await asyncio.sleep(1)
            # await callback(None, s)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    voteurl= 'http://www.iyiou.com/activity/vote_operation/type/15'
    #coroutine in tasks will run 
    tasks = [fetchData(voteurl, pd.processData) for i in range(500)]    
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close() 
