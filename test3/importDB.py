import pymongo

user_info={
    "name":"britneyspears",
    "password":12345,
    "image":"/static/image/britney-spears-wallpaper.jpg",
    "age":32,
    "email":"britneyspears@xxx.com",
    "tweets":[
        {"time":"Nov. 18, 2013",
         "content":"I have always been interested in the scientific discoveries underlying health advances in developing countries. The benefits of such breakthroughs are substantial, with the potential to save hundreds of thousands of lives."
        },

        {"time":"Nov. 1, 2013",
         "content":"How cool is that? I asked him to pay off my student loans if he got me. I guess that is a no go now. ;-)"
        },

        {"time":"Dec. 11, 2013",
         "content":"holy wow!!"
        },

        {"time":"Dec. 15, 2013",
         "content":"Thank you for sharing your experience! It was a fun read :)"
        },

        {"time":"Dec. 20, 2013",
         "content":"I laughed really hard at that. Those are wonderful gifts, and you are an awesome receiver! Very entertaining experience :)"
        },

        {"time":"Dec. 24, 2013",
         "content":"That is amazing! The picture alone is worth it!!"
        }
    ]
}

def importUsers():
    userSets.remove()
    userSets.insert(user_info)

def valid():
    for user in userSets.find():
        print user

conn=pymongo.Connection("localhost",27017)
twitterDB=conn["twitterDB"]
userSets=twitterDB.userSets
importUsers()
valid()

