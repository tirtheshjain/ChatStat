import pandas as pd

def preprocess(file):
    # parse text and create list of lists structure
    # remove first whatsapp info message
    # dataset = data[1:]
    cleaned_data = []
    for line in file:
        # grab the info and cut it out
        line = str(line.decode('utf-8'))
        date = line.split(",")[0]
        line2 = line[len(date):]
        time = line2.split("-")[0][2:]
        line3 = line2[len(time):]
        name = line3.split(":")[0][4:]
        line4 = line3[len(name):]
        message = line4[6:-1] # strip newline charactor

        #print(date, time, name, message)
        cleaned_data.append([date, time, name, message])

    
    # Create the DataFrame 
    df = pd.DataFrame(cleaned_data, columns = ['Date', 'Time', 'Name', 'Message']) 

    # # check formatting 
    # if 0:
    #     print(df.head())
    #     print(df.tail())

    # Save it!
    df.to_csv(r'converted_messages.csv', index=False)
    df = df[df.Message != '']
    df = df[df.Message != '<Media omitted>']

    return df
