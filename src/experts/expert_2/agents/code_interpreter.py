from textwrap import dedent
import func_timeout
import re

def execute_code(code: str, keys=None, timeout_duration=5):
    """
    Executes the given code string and returns the result.

    Parameters
    ----------
    code : str
        The code string to be executed.
    keys : list, optional
        If provided, the function will return a list containing the values of each key after executing the code.
        If not provided, the function will return the value of a variable named 'ans', or None if it does not exist.
    timeout_duration : int, optional
        The maximum allowed time for the code to execute, in seconds. Defaults to 5 seconds.

    Returns
    -------
    result : any
        The result after executing the code. If the code executes successfully, the result is returned;
        if the code execution times out, the string "Error execution time exceeded the limit" is returned;
        if an error occurs during code execution, the string "Error during execution: {e}" is returned, where {e} is the error message.

    Raises
    ------
    Exception
        If an error occurs during code execution, an exception is raised.

    """
    def execute(x):
        try:
            local_namespace = {**locals(), **globals()}
            exec(x, local_namespace, local_namespace)
            if keys is None:
                return local_namespace.get('ans', None)
            else:
                return [local_namespace.get(k, None) for k in keys]
        except Exception as e:
            return f"Error in executing code: {e}"

    try:
        result = func_timeout.func_timeout(timeout_duration, execute, args=(code,))
    except func_timeout.FunctionTimedOut:
        result = "Error execution time exceeded the limit"
    except Exception as e:
        result = f"Error during execution: {e}"

    return result

def floatify_ans(ans):
    """
    Converts the input to a float, if possible.

    Parameters
    ----------
    ans : any
        The input to be converted to a float.

    Returns
    -------
    float or str or None
        The input converted to a float, if possible. If the input is a dictionary, the function attempts to convert the first value to a float.
        If the input is a list or tuple, the function attempts to convert the first element to a float.
        If the input is a string that contains a number, the function extracts the number and converts it to a float.
        If the input cannot be converted to a float, the function returns the input as a string or None if the input is empty.

    """
    if ans is None:
        return None
    elif type(ans) == dict:
        ans = list(ans.values())[0]
    elif type(ans) == bool:
        ans = ans
    elif type(ans) in [list, tuple]:
        if not ans:
            return None
        else:
            try:
                ans = float(ans[0])
            except Exception:
                ans = str(ans[0])
    else:
        try:
            ans = float(ans)
        except Exception:
            if "Error" not in ans:
                # 找到 ans 中的浮点数
                ans = re.findall(r"[-+]?\d*\.\d+|\d+", ans)
                if ans:
                    ans = float(ans[0])
                else:
                    ans = str(ans)
    return ans

def simplify_ans(ans, convert_to_str: bool = True):
    """
    Simplify the answer from a mathematical tools.

    Parameters
    ----------
    ans : various types
        The answer from a mathematical tools, could be various types (e.g., relational, numpy array, etc.)
    convert_to_str : bool, optional
        If True, convert the answer to string type. Default is True.

    Returns
    -------
    various types
        The simplified answer. The return type depends on the input and the `convert_to_str` parameter.
    """

    if 'relational' in str(type(ans)):
        return str(ans)
    elif 'numpy' in str(type(ans)):
        if ans.shape == ():
            # scalar value
            ans = round(float(ans), 2)
        else:
            # array value
            ans = round(float(ans[0]), 2)
        if convert_to_str:
            return str(ans)
        else:
            return ans
    elif not ans:
        return None
    else:
        if type(ans) in [list, tuple]:
            if 'sympy' in str(type(ans[0])):
                try:
                    ans = [round(float(x), 5) for x in ans]
                except Exception:
                    ans = [str(x) for x in ans]
            if len(ans) == 1:
                ans = ans[0]
        else:
            if 'sympy' in str(type(ans)):
                try:
                    ans = round(float(ans), 5)
                except Exception:
                    ans = str(ans)
        if convert_to_str:
            if type(ans) is str:
                return ans
            else:
                return str(round(ans, 5))
        else:
            return ans

class BaseCodeInterpreter:
    def __call__(self, code: str, keys=None, timeout_duration=5):
        return execute_code(code, keys, timeout_duration)

class MathCodeInterpreter:
    def __init__(self) -> None:
        self.code_interpreter_agent = BaseCodeInterpreter()

    def __call__(self, code) -> int | float | None:
        ans = self.code_interpreter_agent(code=code, timeout_duration=5)
        if type(ans) is str:
            ans = simplify_ans(floatify_ans(ans), convert_to_str=True)
        return ans



class VerifyAndVote:
    def __init__(self) -> None:
        self.base_code_interpreter = BaseCodeInterpreter()
    
    def __call__(self, answers: list[str], code: str) -> str:
        verified_answers = []
        for ans in answers:
            # Step 1. The original code may lack the 'Verify' function.
            verify_code = add_verify_function(code, ans)
            # Step 2. Execute the code with the Verify function.
            try:
                result = self.base_code_interpreter(code=verify_code, timeout_duration=5)
                if result:
                    # Vote 2 times to make the result more reliable
                    verified_answers.extend([ans]*2)
                else:
                    verified_answers.append(ans)
            except:
                verified_answers.append(ans)
        # Step 3. Vote for the most likely correct answer.
        return simple_vote(verified_answers)

def add_verify_function(code_string, value):
    if code_string.endswith(f"result = Verify({value})"):
        return code_string

    try:
        # 找到最后一个'\n'
        index = code_string.rfind('\n')
        # 删除index之后的内容
        code_string = code_string[:index]
        # 添加result = Verify(value)
        code_string = code_string + f"result = Verify({value})"
        return code_string
    except Exception as e:
        return f"Error during execution: {e}"

def auto_round(num_str):
    import re
    match = re.search(r'(\.(\d*?)(9{3,}|0{3,}|1{3,}|2{3,}|3{3,}|4{3,}|5{3,}|6{3,}|7{3,}|8{3,})\d*)', num_str)
    if match:
        precision = len(match.group(2))
        num = str(round(float(num_str), precision))
    else:
        num = num_str
    return num

def simple_vote(values):
    # Vote counting
    vote_count = {}
    max_vote = 0
    max_value = "-5201314"
    for value in values:
        if not isinstance(value, str):
            value = str(value)
        vote_count[value] = vote_count.get(value, 0) + 1
        if vote_count[value] > max_vote:
            max_vote = vote_count[value]
            max_value = value

    max_value = auto_round(max_value)  # Round the value
    return max_value