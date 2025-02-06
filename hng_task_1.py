from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
app.json.sort_keys=False

@app.errorhandler(400)
def alphabet_passed():
    is_error = True
    response = jsonify({'number': 'alphabet',
                'error': is_error})
    
    return response, 400

@app.route('/')
def welcome():
    return 'HNG Backend Stage 1 Task'


@app.route('/api/classify-number', methods = ['GET'])
def classify_num():
    '''
    Performs three tests:
        i. prime test
        ii. perfect test
        iii. armstrong test
        iv. parity test
    
    Returns:
        i. The proprties of the number from the test
        ii. A funfact from number api
    '''
    input_num = request.args.get('number', type=int) #Variable to store input
    
    try:
        
        input_num = int(input_num)

        if input_num < 0:
            raise ValueError("Negative Number")

        ## TODO-1: Prime test - input number is positive, greater than 0
        divisors = []
        is_prime = False #assume a number is not a prime number
        for divisor in range(1,input_num):
            if input_num%divisor == 0:
                divisors.append(divisor)
            # if len(divisors) > 3:
            #         break
        if len(divisors) < 2:
            is_prime = True
        
        
        ## TODO-2: Perfect test - sum of divisors should equal positive number
        is_perfect = False
        if sum(divisors) == input_num:
            is_perfect = True


        ## TODO-3: Armstrong test - sum of each digits raised to the number of digits is equal to the input positive number
        arm_num = input_num.__repr__()
        len_num = len(arm_num)

        digit_sum = 0
        arm_sum = 0
        is_armstrong = False
        for n in arm_num:
            arm_sum += int(n)**len_num
            digit_sum += int(n)
        if arm_sum == input_num:
            is_armstrong = True


        ## TODO-4: Parity test - check if an integer is odd or not
        is_odd = True
        if input_num%2 == 0:
            is_odd = False

        ## Number Properties
        property = []
        if is_armstrong:
            property.append("armstrong")
        if is_odd:
            property.append("odd")
        else:
            property.append("even")

        ## TODO-5: Funfact API - get an interesting information about the number
        api_url = 'http://numbersapi.com/'+str(input_num)+'/math?json'
        response = requests.get(api_url)
        response = response.json()

        
        ## TODO-6: Return the response
        response = jsonify({"number": input_num,
                        "is_prime": is_prime,
                        "is_perfect": is_perfect,
                        "properties": property,
                        "digit_sum": digit_sum,
                        'fun_fact': response['text']})
        
        return response
        
    except TypeError:
            is_error = True
            response = jsonify({'number': 'alphabet',
                        'error': is_error})
            
            return flask.redirect('/404')
    
    except ValueError:
            is_error = True
            response = jsonify({'number': 'negative',
                                'error': is_error})
            
            return response

    

if __name__ == '__main__':
    app.run(debug=True)
    



    
    







