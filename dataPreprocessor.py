import pandas as pd

def preprocess(file):
    # parse text and create list of lists structure
    processed_data = []
    for line in file:
        # grab the info and cut it out
        line = str(line.decode('utf-8'))
        date = line.split(",")[0]
        line = line[len(date):]
        time = line.split("-")[0][2:]
        line = line[2 + len(time):]
        user = line.split(":")[0][2:]
        line = line[2 + len(user):]
        message = line[2:-1] # strip newline character
        processed_data.append([date, time, user, message])

    # Create the DataFrame 
    df = pd.DataFrame(processed_data, columns = ['Date', 'Time', 'User', 'Message']) 

    # filter the DataFrame to remove whatsapp info message
    df = df[df.Message != '']
    

    return df
