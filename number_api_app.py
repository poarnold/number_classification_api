from flask import Flask, request, jsonify
import requests # to access external apis
from flask_cors import CORS #to allow cross origin resource sharing

app = Flask(__name__)
app.json.sort_keys=False
CORS(app)


@app.route('/')
def welcome():
    # Default Homepage response for the application endpoint
    return 'HNG Backend Stage 1 Task'


@app.route('/api/classify-number', methods = ['GET'])
def classify_num():
    '''
    This Flask Function returns the properties of a positive integer entry. Valid inputs are positive integers. 
    The function performs four tests on the inputs and returns their properties.
        i. prime test
        ii. perfect test
        iii. armstrong test
        iv. parity test

    A basic error check is implemented to return response when a different object type is inputted.
        
    Parameters
    ----------
        number (int): positive integer

    Returns
    -------
         json,  {"number": input num,
                "is_prime": prime test,
                "is_perfect": perfect test,
                "properties": [armstrong test, parity test],
                 "digit_sum": sum of digits,
                "fun_fact": response from <http://numbersapi.com/'+str(input num)+'/math?json>}

    ''' 
    
    input_num = request.args.get('number') #Variable to store input
    
    try:
        
        ## Check missing inputs and invalid inputs
        if input_num is None:
            return jsonify({'number': 'missing. Missing required parameter - positive number', 'error':True}), 400
        
        if not input_num.isdigit():
            try:
                if int(input_num) < 0:
                    return jsonify({'number': 'negative', 'error': True }), 400
            except:
                return jsonify({'number': 'alphabet', 'error': True}), 400
        
                     
        input_num = int(input_num)

        is_positive = 1
        if input_num < 0:
            is_positive = 0
            input_num = abs(input_num)

        ## Prime test - input number is positive, greater than 0
        divisors = []
        is_prime = False #assume a number is not a prime number
        for divisor in range(1,input_num):
            if input_num%divisor == 0 and is_positive:
                divisors.append(divisor)
            # if len(divisors) > 3:
            #         break
        if len(divisors) < 2 and len(divisors) != 0:
            is_prime = True
        
        
        ## Perfect test - sum of divisors should equal positive number
        is_perfect = False
        if sum(divisors) == input_num:
            is_perfect = True


        ## Armstrong test - sum of each digits raised to the number of digits is equal to the input positive number
        arm_num = input_num.__repr__()
        len_num = len(arm_num)

        digit_sum = 0
        arm_sum = 0
        is_armstrong = False
        
        for n in arm_num:
            arm_sum += int(n)**len_num
            digit_sum += int(n)
        if arm_sum == input_num and is_positive:
            is_armstrong = True


        ## Parity test - check if an integer is odd or not
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

        ## Funfact API - get an interesting information about the number
        api_url = 'http://numbersapi.com/'+str(input_num)+'/math?json'
        response = requests.get(api_url)
        response = response.json()

        
        ## Return the response
        response = jsonify({"number": input_num,
                        "is_prime": is_prime,
                        "is_perfect": is_perfect,
                        "properties": property,
                        "digit_sum": digit_sum,
                        'fun_fact': response['text']})
        
        return response
        
    
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False)
    