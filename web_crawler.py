import os
import re
import urllib.request
import requests
import time
import sys
from requests_html import HTML
from bs4 import BeautifulSoup

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':RC4-SHA'

overall_user_push={}
overall_user_boo={}
overall_image_url=[]
overall_keyword_image_url=[]
def fetch(url):
    time.sleep(0.4)
    response=requests.get(url=url,cookies={'over18':'1'})
    if response.status_code != 200:  #回傳200代表正常
        print('Invalid url:', response.url)
        return None
    else:
        return response
    
def article(content,counter):
    output_all_file = open("all_articles.txt", "a",encoding='utf8')
    output_popular_file = open("all_popular.txt", "a",encoding='utf8')

    fixed='https://www.ptt.cc'
    end_flag=0
    soup=BeautifulSoup(content,'html.parser')
    all_page_elements=soup.find('div','btn-group btn-group-paging')
    all_meta_data_divs=soup.find_all('div','r-ent')
    post_page=all_page_elements.find_all('a')[2]['href']
    
    for meta_data in all_meta_data_divs:
        if meta_data.find('a'):
            push_information=meta_data.find('div','nrec').string
            hyper_link=fixed+meta_data.find('a')['href']
            title=meta_data.find('a').string
            dates=int(meta_data.find("div", {"class": "date"}).string.strip().replace('/',''))
            if title!=None and len(title)>3:
                classification=title[1:3]
                title=title.replace(',',' ')
            if hyper_link!=None and title!=None and dates!=None and len(title)>3 and classification!=None and classification!="公告":
                if counter==0:
                    if dates<800:
                        output_all_file.write(str(dates)+","+str(title)+","+str(hyper_link)+"\n")
                        if push_information!=None and push_information=="爆":
                            output_popular_file.write(str(dates)+","+str(title)+","+str(hyper_link)+"\n")
                elif counter>100 and dates<105:
                    end_flag=1
                    return end_flag,None
                else:
                    output_all_file.write(str(dates)+","+str(title)+","+str(hyper_link)+"\n")
                    if push_information!=None and push_information=="爆":
                        output_popular_file.write(str(dates)+","+str(title)+","+str(hyper_link)+"\n")
                 
                    
    output_all_file.close()
    return end_flag,fixed+post_page
def like_boo_count(content):
    likes=0
    boos=0
    soup=BeautifulSoup(content,'html.parser')
    all_meta_data_divs=soup.find_all('div','push')
    for meta_data in all_meta_data_divs:
        if meta_data.find('span', 'push-tag') and meta_data.find('span','push-userid'):
            information = meta_data.find('span', 'push-tag').string.strip(' \t\n\r')
            user_name=meta_data.find('span','push-userid').string.strip(' \t\n\r')
            current_item=[]
            if information=="推":
                likes+=1
                if user_name not in overall_user_push:
                    overall_user_push[user_name]=1
                else:
                    overall_user_push[user_name]+=1
                    
            elif information=="噓":
                boos+=1
                current_item.append(user_name)
                current_item.append("boo")
                if user_name not in overall_user_boo:
                    overall_user_boo[user_name]=1
                else:
                    overall_user_boo[user_name]+=1
    return likes,boos
def get_image_url(content):
    pattern=re.compile("^(http).*((\.jpg)|(\.jpeg)|(\.png)|(\.gif))$")

    soup=BeautifulSoup(content,'html.parser')
    all_meta_data_divs=soup.find_all('a')
    for meta_data in all_meta_data_divs:
        current_url=meta_data.string
        if current_url!=None:
            match_result=pattern.match(current_url)
            
            if match_result:
                overall_image_url.append(current_url)
def get_keyword_image_url(content):
    pattern=re.compile("^(http).*((\.jpg)|(\.jpeg)|(\.png)|(\.gif))$")

    soup=BeautifulSoup(content,'html.parser')
    all_meta_data_divs=soup.find_all('a')
    for meta_data in all_meta_data_divs:
        current_url=meta_data.string
        if current_url!=None:
            match_result=pattern.match(current_url)
            
            if match_result:
                overall_keyword_image_url.append(current_url)
def check_keyword(content,keyword):
    pattern=re.compile("^[ ]*(<){1}")
    overall_results=[]
    find_start_result=content.find("作者")
    find_end_result=content.find("<span class=\"f2\">")
    if find_start_result==-1 or find_end_result==-1:
        return False
    total_string=content[find_start_result:find_end_result]
    soup=BeautifulSoup(total_string,'html.parser')
    total_result=soup.prettify()
    overall_strings=total_result.split('\n')
    for current_string in overall_strings:
        match_result=pattern.match(current_string)
        if not match_result:
            overall_results.append(current_string)
            
    for current_result in overall_results:#剩這裡
        if current_result.find(keyword)!=-1:
            #print(current_result,keyword)
            return True
    #print(total_string)
    #print(find_start_result,find_end_result)
    
    return False
if __name__=='__main__':
    if len(sys.argv)<2:
        print("No command line input argument found, please look at the readme file.")
    choice=sys.argv[1]
    if choice=="crawl":
        tStart = time.time()
        if os.path.exists("all_articles.txt"):
            os.remove("all_articles.txt")
        if os.path.exists("all_popular.txt"):
            os.remove("all_popular.txt")
        end_flag=0
        current_url='https://www.ptt.cc/bbs/Beauty/index3150.html' #3150至今
        current_response=fetch(current_url)
        counter=0
        if current_response!=None:
            contents=current_response.text
            if contents!=None:
                end_flag,post_page=article(contents,counter)
                counter+=1
                while post_page!=None and end_flag==0:
                    current_response=fetch(post_page)
                    contents=current_response.text
                    end_flag,post_page=article(contents,counter)
                    counter+=1
        tEnd=time.time()
        print(tEnd-tStart)
    elif choice=="push":
        if len(sys.argv)<4:
            print("Too less command line input arguments! Start_date and end_date are required.")
        start_date=int(sys.argv[2])
        end_date=int(sys.argv[3])
        
        tStart = time.time()
        
        like_counter=0
        boo_counter=0
        file_name="push["+str(start_date)+"-"+str(end_date)+"].txt"
        
        if os.path.exists(file_name):
            os.remove(file_name)
        
        output_result_file=open(file_name,"a",encoding='utf8')
        
        with open("all_articles.txt",encoding='utf8') as f:
            content=f.readlines()
        overall_date=[]
        overall_title=[]
        overall_url=[]
        
        flag_start=0
        flag_end=0
        start_index=-1
        end_index=-1
            
        for i in range(0,len(content)):
            temp_line=content[i].split(',')
            overall_date.append(temp_line[0])
            overall_title.append(temp_line[1])
            overall_url.append(temp_line[2].replace('\n',''))

        for i in range(0,len(content)):
            if flag_start==0 and int(overall_date[i])>=start_date:
                start_index=i
                flag_start=1
            if int(overall_date[i])==end_date:
                end_index=i
            if flag_end==0 and end_index==-1 and int(overall_date[i])>end_date:
                end_index=i-1
                flag_end=1
        
        for i in range(start_index,end_index+1):
            response=fetch(overall_url[i])
            if response!=None:
                article_content=response.text
                likes,boos=like_boo_count(article_content)
                like_counter+=likes
                boo_counter+=boos

    
        overall_user_push=sorted(overall_user_push.items(), key=lambda kv: kv[0])
        overall_user_boo=sorted(overall_user_boo.items(), key=lambda kv: kv[0])
        overall_user_push=sorted(overall_user_push, key=lambda kv: kv[1],reverse=True)
        overall_user_boo=sorted(overall_user_boo, key=lambda kv: kv[1],reverse=True)


        output_result_file.write("all like: "+str(like_counter)+"\n")
        output_result_file.write("all boo: "+str(boo_counter)+"\n")
        
        for i in range(0,10):
            output_result_file.write("like #"+str(i+1)+": "+str(overall_user_push[i][0])+" "+str(overall_user_push[i][1])+"\n")

        for i in range(0,10):
            output_result_file.write("boo #"+str(i+1)+": "+str(overall_user_boo[i][0])+" "+str(overall_user_boo[i][1])+"\n")

        output_result_file.close()
        tEnd=time.time()
        print(tEnd-tStart)
    elif choice=="popular":
        if len(sys.argv)<4:
            print("Too less command line input arguments! Start_date and end_date are required.")
        start_date=int(sys.argv[2])
        end_date=int(sys.argv[3])
        
        tStart = time.time()
        popular_counter=0

        file_name="popular["+str(start_date)+"-"+str(end_date)+"].txt"
        
        if os.path.exists(file_name):
            os.remove(file_name)

        output_result_file=open(file_name,"a",encoding='utf8')
        
        with open("all_popular.txt",encoding='utf8') as f:
            content=f.readlines()
            
        overall_date=[]
        overall_title=[]
        overall_url=[]
        
        flag_start=0
        flag_end=0
        start_index=-1
        end_index=-1
            
        for i in range(0,len(content)):
            temp_line=content[i].split(',')
            overall_date.append(temp_line[0])
            overall_title.append(temp_line[1])
            overall_url.append(temp_line[2].replace('\n',''))

        for i in range(0,len(content)):
            if flag_start==0 and int(overall_date[i])>=start_date:
                start_index=i
                flag_start=1
            if int(overall_date[i])==end_date:
                end_index=i
            if flag_end==0 and end_index==-1 and int(overall_date[i])>end_date:
                end_index=i-1
                flag_end=1

        popular_counter=end_index-start_index+1
        
        for i in range(start_index,end_index+1):
            response=fetch(overall_url[i])
            if response!=None:
                article_content=response.text
                get_image_url(article_content)
        
        output_result_file.write("number of popular articles: "+str(popular_counter)+"\n")
        for i in range(0,len(overall_image_url)):
            output_result_file.write(overall_image_url[i]+"\n")
        output_result_file.close()
        tEnd=time.time()
        print(tEnd-tStart)
    elif choice=="keyword":
        if len(sys.argv)<5:
            print("Too less command line input arguments! Keyword, start_date and end_date are required.")
        keyword=sys.argv[2]
        start_date=int(sys.argv[3])
        end_date=int(sys.argv[4])

        keyword="正妹"
        start_date=505
        end_date=1101
        
        tStart = time.time()

        file_name="keyword("+keyword+")["+str(start_date)+"-"+str(end_date)+"].txt"
        
        if os.path.exists(file_name):
            os.remove(file_name)

        output_result_file=open(file_name,"a",encoding='utf8')
        
        with open("all_articles.txt",encoding='utf8') as f:
            content=f.readlines()

        overall_date=[]
        overall_title=[]
        overall_url=[]
        
        flag_start=0
        flag_end=0
        start_index=-1
        end_index=-1
            
        for i in range(0,len(content)):
            temp_line=content[i].split(',')
            overall_date.append(temp_line[0])
            overall_title.append(temp_line[1])
            overall_url.append(temp_line[2].replace('\n',''))

        for i in range(0,len(content)):
            if flag_start==0 and int(overall_date[i])>=start_date:
                start_index=i
                flag_start=1
            if int(overall_date[i])==end_date:
                end_index=i
            if flag_end==0 and end_index==-1 and int(overall_date[i])>end_date:
                end_index=i-1
                flag_end=1

        for i in range(start_index,end_index+1):
            response=fetch(overall_url[i])
            if response!=None:
                article_content=response.text
            
                find_keyword=check_keyword(article_content,keyword)
                if find_keyword:
                    get_keyword_image_url(article_content)

        for i in range(0,len(overall_keyword_image_url)):
            output_result_file.write(overall_keyword_image_url[i]+"\n")
        output_result_file.close()
        tEnd=time.time()
        print(tEnd-tStart)
        