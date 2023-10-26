from sd.sd4free import SD

if __name__ == '__main__':
    # instance = SD("s4f")
    # re = instance.generator(prompt="cat")
    # instance = SD("diffle")
    # re = instance.generator(prompt="cat")
    # instance = SD("openskyml")
    # re = instance.generator(prompt="cat")
    instance = SD("wizmodel")
    re = instance.generator(prompt="cat")
    print(re)
