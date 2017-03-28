# import graphlab as gl
from newspaper import Article

def extract(url):
    of_interest = [
        'meta_keywords',
        'text',
        'title',
        'top_image',
        'authors',
        'keywords'
    ]
    try:
        a = Article(url)
        a.download()
        a.parse()

        # this is a useful freebe that uses NLTK to extract keywords
        # you can comment this out if you don't want to rely on NLTK
        a.nlp()

    # We are working with an external site and a lot of things can go wrong
    # We want to know about it but we don't want it to mess up the execution.
    except Exception as e:
        print "Exception: {} occured at url: \t{} ".format(e, url)

        # We will be able to deal with the missing values later
        return {}

    return dict([
            # converts lists into dicts and leaves scalars untouched
            (k, v) if not isinstance(v, list) else (k, {x: 1 for x in v})

            # iterate over the properties of the Article object
            for k, v in vars(a).iteritems()

            # keep only ones that we want
            if k in of_interest
        ])

print (extract("http://mashable.com/2013/01/15/tony-hawk-operation-smile"))

