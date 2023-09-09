#BICEP CURL UP CODE
def curl_counter_logic(angle, stage, counter):
    if angle > 160:
        stage = "down"
    if angle < 30 and stage == 'down':
        stage = "up"
        counter += 1
        print(counter)
    return stage, counter