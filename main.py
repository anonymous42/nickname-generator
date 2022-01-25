# TODO: 1. load model from json file
# 2. generate length and first letter
# 3. generate each new letter based on probabilities

import json
import random


class NicknameGenerator:
    def __init__(self, model_filename="model.json"):
        """
        Load model
        """
        self.model_filename = model_filename
        self.nickname = "Name is not generated!"
        try:
            with open(model_filename, "r") as model_file:
                self.model = json.load(model_file)
        except Exception as e:
            print(f"File ./{model_filename} invalid or does not exist!")
            exit()

    def __choose(self, prob_dict):
        return random.choices(list(prob_dict.keys()),
                              list(prob_dict.values()))[0]

    def __sub_train(self, prob_dict, good_value):
        add_points = len(list(prob_dict.keys())) - \
            list(prob_dict.values()).count(0)
        good_prob = prob_dict[good_value]
        if not good_prob == 100000:
            prob_dict[good_value] += add_points
            for i in list(prob_dict.keys()):
                prob_dict[i] -= 0 if prob_dict[i]-1 < 0 else 1
        assert sum(list(prob_dict.values())) == 100000
        return prob_dict

    def generate(self):
        """
        Generate new nickname
        """
        # Generate length
        length_prob = self.model[0]
        self.length_var = int(self.__choose(length_prob))

        # Generate first letter
        self.nickname = chr(random.randint(97, 122))

        # Generate all next letters
        letter_prob = self.model[1]
        for i in range(self.length_var-1):
            self.nickname += self.__choose(letter_prob[self.nickname[i]])

        return self.nickname

    def train(self, good_nickname):
        # change self.model and write it to model file
        self.model[0] = self.__sub_train(self.model[0],
                                         str(len(good_nickname)))
        assert sum(list(self.model[0].values())) == 100000

        for i in range(len(good_nickname)-1):
            self.model[1][good_nickname[i]] = self.__sub_train(
                                               self.model[1][good_nickname[i]],
                                               good_nickname[i+1])
            assert sum(list(
                self.model[1][good_nickname[i]].values()
                            )) == 100000

        with open(self.model_filename, "w") as model_file:
            json.dump(self.model, model_file)


nickgen = NicknameGenerator()
while True:
    nickname = nickgen.generate()
    print(f"Is this nickname good? [Yes, Quit]\n{nickname}")
    answer = input()
    if answer == 'Y':
        nickgen.train(nickname)
    if answer == 'Q':
        break
