import re

class Utils:
    @classmethod
    def remove_before_first_space(cls, string):
        # Check if the string contains a space
        if ' ' in string:
            # Find the index of the first space that is not within brackets
            index = 0
            bracket_count = 0
            for i, char in enumerate(string):
                if char == '[':
                    bracket_count += 1
                elif char == ']':
                    bracket_count -= 1
                elif char == ' ' and bracket_count == 0:
                    index = i
                    break
            return string[:index]
        else:
            return string  # Return the original string if there's no space

    @classmethod
    def replace_non_alphanumeric(cls, text):
        # Define the regular expression pattern
        pattern = r'[^a-zA-Z0-9\s\[\]](?![^\[]*\])'

        # Replace matching characters with an empty string
        return re.sub(pattern, '', text)

if __name__ == '__main__':
    # Test the class method
    string = "Remove everything before the first space"
    result = Utils.remove_before_first_space(string)
    print(result)  # Output: "everything before the first space"

        # Test the function
    text = "[Order Details] should not be replaced since its a square bracket with a open and close bracket. However [Orders should be replaced since it doesn't have one. Same with \"Order and (Orders"
    result = Utils.replace_non_alphanumeric(text)
    print(result)