for i in range(1, 121):
    try: 
       filenames = ['input_' + str(i) + '.data']
       with open('input.data', 'a') as outfile:
           for fname in filenames:
               with open(fname) as infile:
                   outfile.write(infile.read())
    except:
        pass