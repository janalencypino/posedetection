#BELOW IS ALL EXERCISE COUNTER LOGIC

#BICEP CURL UP 
def curl_counter_logic(angle, stage, ave, counter):
    if angle > 160:
        stage = "down"
    if angle < 30 and stage =='down':
        stage="up"
        counter +=1
        if inside > angle:
            inside = angle
    if angle > 30 and stage == "up":
        ave += inside
        inside = 31
        stage = "down"
        print(ave)

#SQUATS 
def squats_counter_logic(angle, stage, counter):
    if angle <= 90:
        stage = "down"
    if angle >= 160 and stage =='down':
        stage="up"
        counter +=1
    return stage, counter

#PUSH-UP
def pushup_counter_logic(angle, angle2, stage, counter):
    if angle <= 70:
        stage = "down"
    elif stage =='down' and angle >= 160:
        stage="up"
        if angle2 > 160 and angle2 < 180:
            stage="incorrect position"
        else: 
            counter +=1     
            print(counter)
    return stage, counter

#PLANK
def plank_counter_logic(angle, angle2, stage, counter):
    if angle < 90:
        stage = "adjust your arms"
        if angle2 < 170:
            stage="lower your hip position"
        elif angle2 >= 170:
            stage="down" 
            counter +=1
            print(counter)
    return stage, counter