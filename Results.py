from boto.mturk.connection import MTurkConnection
from itertools import chain
from datetime import datetime
import csv

def zerolistmaker(n):
    listofzeros = [0.0] * n
    return listofzeros

def formAns(ans_obj, ANP):
    ans_tuple = map(lambda a: (ANP, a.fields), ans_obj)
    return dict(ans_tuple)

def parseAnswer(form, hit_anp_dict):
    # Create a dictionary to hold form responses
    form_dict = {}

    # Stick form response in a dict
    for a in form.answers:
        hitId = form.HITId
        ANP = hit_anp_dict[hitId]
        form_ans = formAns(a, ANP)
        for r in form_ans.keys():
            form_dict[r] = list()
            for value in form_ans.values():
                form_dict[r].append(value)

    # Form responses where no data is recorded will have a None value
    return form_dict

def reviewAssignment(a, hit_anp_dict, mturk=None, auto_approve=False, redownload=False):
    answer_list = list()
    aid = a.AssignmentId
    status = a.AssignmentStatus
    if status == "Submitted":
        if auto_approve:
            mtc.approve_assignment(aid)
        answer_list.append(parseAnswer(a, hit_anp_dict))
    if a.AssignmentStatus == "Approved" and redownload:
        answer_list.append(parseAnswer(a, hit_anp_dict))
    return answer_list

if __name__ == '__main__':

    #emotions
    emotions=['Ecstacy',
              'Joy',
              'Serenity',
              'Admiration',
              'Trust',
              'Acceptance',
              'Terror',
              'Fear',
              'Apprehension',
              'Amazement',
              'Surprise',
              'Distraction',
              'Grief',
              'Sadness',
              'Pensiveness',
              'Loathing',
              'Disgust',
              'Boredom',
              'Rage',
              'Anger',
              'Annoyance',
              'Vigilance',
              'Anticipation',
              'Interest']

    ANP_set = set()
    reader = csv.reader(open('dict.csv'))
    hit_anp_dict = {}
    for row in reader:
        key = row[0]
        if key in hit_anp_dict:
        # implement your duplicate row handling here
            pass
        hit_anp_dict[key] = row[1]
        ANP_set.add(row[1])

    ratings = range(1,25)

    d = dict(zip(emotions, ratings))

    # File path to downloads
    res_dir = "results/sandbox/"

    # Record start time
    start_time = datetime.now().strftime("%s")

    ACCESS_ID =''
    SECRET_KEY = ''
    HOST = 'mechanicalturk.sandbox.amazonaws.com'

    mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                          aws_secret_access_key=SECRET_KEY,
                          host=HOST)

    # Download reviewable HITs
    reviewable_assignments = list()
    hit_list = list(hit_anp_dict.keys())
    for h in hit_list:
        max_page = False
        m = 10
        p = 1
        while not max_page:
            assignments = mtc.get_assignments(h, page_size=m, page_number=p)
            if len(assignments) > 0:
                reviewable_assignments.extend(assignments)
                if(len(assignments) < m):
                    max_page = True
                else:
                    p += 1
            else:
                max_page =True

    # Review assignments
    response_list = list()
    for a in reviewable_assignments:
        submitted_work = reviewAssignment(a, hit_anp_dict, mtc, redownload=True)
        if len(submitted_work) > 0:
            response_list.append(submitted_work)
    responses = list(chain.from_iterable(response_list))
    print responses

    anp_keys = map(lambda i: i,  ANP_set)
    anp_dict = dict.fromkeys(anp_keys, None)

    for ans_tuple in responses:
        cur_key = ans_tuple.keys()
        cur_val = ans_tuple.values()
        if cur_key[0] in anp_dict:
            anp_dict[cur_key[0]] = zerolistmaker(len(emotions))
            for value in cur_val[0][0]:
                emotion = value.split('|')
                for i in range(0, len(emotion)):
                    val = d[emotion[i]]
                    anp_dict[cur_key[0]][val-1] += 1

    anp_emotions_list = emotions
    anp_emotions_list.insert(0, 'ANP')

    # Output file, name simply based on the time it is created
    if len(responses) > 0:
        f = res_dir+start_time+".csv"
        with open(f,'wb') as fp:
            print >>fp, ", ".join(anp_emotions_list)
            w = csv.writer(fp)
            for k, v in anp_dict.iteritems():
                w.writerow([k] + v)

        fp.close()
