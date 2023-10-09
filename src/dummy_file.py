### telegram imports###

# track if feature succesfully applied
flag= False

dummy_num = 5


async def process_user_response(x):

    if x == dummy_num:
        flag = False
        ## some operations on x ##
        return x

    else:
        flag = True
        ## some operations on x##
        return "boo"


async def dummy_bot_feature(a):
    user_response = a

    text = process_user_response(a)

    if flag:
        # send message via bot

    else:
        # send some another message via bot


if __name__ == "__main__":




