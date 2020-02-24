from random import random
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
import random
app = Flask(__name__)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.My_recipick_project  # 'dbsparta'라는 이름의 db를 만듭니다.


client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('s_official_card.html')

##################################### 레시피 API 생성 ######################################

@app.route('/s_official_recipes', methods=['GET'])
def officialListing():
    soomi_official = list(db.soomis_all_recipes.find({'category':'공식 레시피'}, {'_id': 0}))
    return jsonify({'result': 'success', 'soomis_official': soomi_official})

@app.route('/s_follow_recipes', methods=['GET'])
def followListing():
    soomi_follow = list(db.soomis_all_recipes.find({'category':'따라하기 레시피'}, {'_id': 0}))
    return jsonify({'result': 'success', 'soomis_follow': soomi_follow})

##################################### 레시피검색 API ######################################
# 세미님 git_hub code 참고
# soomis_all_recipes db에서 s_official_recipe의 정보와 일치하는 data를 넘겨준다
@app.route('/search_soomi_official', methods=['GET'])
def search_soomi_official_view():
    recipe_title_receive = request.args.get('recipe_title_give')
    soomi_official_info = list(db.soomis_all_recipes.find({'category':'공식 레시피','title':{'$regex':recipe_title_receive}}, {'_id': 0}))
    return jsonify({'result': 'success', 'soomis_official_info': soomi_official_info})

# soomis_all_recipes s_follow_recipe db에서 정보와 일치하는 data를 넘겨준다
@app.route('/search_soomi_follow', methods=['GET'])
def search_soomi_follow_view():
    recipe_title_receive = request.args.get('recipe_title_give')
    soomi_follow_info = list(db.soomis_al_recipes.find({'category':'따라하기 레시피','title':{'$regex':recipe_title_receive}}, {'_id': 0}))
    return jsonify({'result': 'success', 'soomis_follow_info': soomi_follow_info})
    ##################################### 레시피 업데이트 API ######################################

@app.route('/save_follow_recipe', methods=['POST'])
def save_follow_recipe():
    # 클라이언트로부터 데이터를 받는 부분
    email_receive = request.form['email_give']
    # 요청할 때 함께 줄 데이터
    image_receive = request.form['image_give']
    title_receive = request.form['title_give']
    posting_day_receive = request.form['posting_day_give']
    description_receive = request.form['description_give']
    author_receive = request.form['author_give']
    url_receive = request.form['url_give']

    # test
    #
    save_my_recipe = {
        'email': email_receive,
        'image': image_receive,
        'title': title_receive,
        'posting_day': posting_day_receive,
        'description': description_receive,
        'author': author_receive,
        'url': url_receive,
    }
    db.save_follow_recipes.insert_one(save_my_recipe)

    return jsonify({'result': 'success'})
##################################### 레시피 랜덤 뿌리기 API #####################################

# 추천 레시피 랜덤으로 뽑아서 보여주기
# for g in range(100):
#     soomi_follow_recipe = list(db.soomis_follow_recipes.find({'author':'수미네반찬 블로그'}, {'_id': 0}))
#     good = (random.sample(soomi_follow_recipe, 10))
#     for i in range(10):
#         numData = i
#     good = good[numData]['title']

# @app.route('/s_rand_follow_recipes', methods=['GET'])
# def random_recipes():
#     for g in range(4):
#         soomi_follow_recipe = list(db.soomis_all_recipes.find({'author':'수미네반찬 블로그'}, {'_id': 0}))
#         soomi_random_recipe = (random.sample(soomi_follow_recipe, 5))
#         for i in range(10):
#             numData = i
#         soomi_random_recipe = soomi_random_recipe[numData]['title']
#         print(soomi_random_recipe)
#     return jsonify({'result': 'success', 'recommend_recipes': soomi_random_recipe})


if __name__ == '__main__':
    app.run('localhost', port=8000, debug=True)
# def get_context_data(self, **kwargs):
#     context = super(PostLV, self).get_context_data(**kwargs)
#     paginator = context['paginator']
#     page_numbers_range = 10
#     max_index = len(paginator.page_range)
#
#     page = self.request.GET.get('page')
#     current_page = int(page) if page else 1
#
#     start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
#     end_index = start_index + page_numbers_range
#     if end_index >= max_index:
#         end_index = max_index
#
#     page_range = paginator.page_range[start_index:end_index]
#     context['page_range'] = page_range
#     return context