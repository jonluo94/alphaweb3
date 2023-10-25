from sd.sd4free import SD

if __name__ == '__main__':
    instance = SD("s4f")
    re = instance.generator(prompt="breathtaking selfie photograph of astronaut floating in space, earth in the background. award-winning, professional, highly detailed")
    instance = SD("diffle")
    re = instance.generator(prompt="cat")
    instance = SD("openskyml")
    re = instance.generator(prompt="cat")
    print(re)
