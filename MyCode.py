from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer
from boto.mturk.qualification import Qualifications, Requirement
from boto.mturk.layoutparam import LayoutParameter
from boto.mturk.layoutparam import LayoutParameters
import csv, random, flickrapi

api_key = 'ac0d3cf61f420ccc89928aa654241771'
api_password = '89b53de03059da8e'

ACCESS_ID ='AKIAJAR2Y4GOFK2QAABQ'
SECRET_KEY = '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'
HOST = 'mechanicalturk.sandbox.amazonaws.com'

if __name__ == '__main__':
    flickrclient = flickrapi.FlickrAPI(api_key, api_password)
    flickrclient.authenticate_via_browser(perms='read')

    mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)

    title = 'Map images to emotions'
    description = ('Given an image identify what emotion'
               ' the image depicts and whether the ANP is correct')
    keywords = 'image, emotions, ANP'

    ratings =[('Ecstacy','1'),
          ('Joy','2'),
          ('Serenity','3'),
          ('Admiration','4'),
          ('Trust','5'),
          ('Acceptance','6'),
          ('Terror','7'),
          ('Fear','8'),
          ('Apprehension','9'),
          ('Amazement','10'),
          ('Surprise','11'),
          ('Distraction','12'),
          ('Grief','13'),
          ('Sadness','14'),
          ('Pensiveness','15'),
          ('Loathing','16'),
          ('Disgust','17'),
          ('Boredom','18'),
          ('Rage','19'),
          ('Anger','20'),
          ('Annoyance','21'),
          ('Vigilance','22'),
          ('Anticipation','23'),
          ('Interest','24'),
          ('None of these','25')]

    ANP_dict = dict()
    f = open('/home/prateek/Downloads/mvso_mapping_tagonly/testFileANP.txt')
    csv_f = csv.reader(f)

    for row in csv_f:
        elem = row[0].split(' ')
        lookUp = elem[0].split('/')
        photoId = lookUp[2].split('.')
        if lookUp[1] in ANP_dict:
            ANP_dict[lookUp[1]].add(photoId[0])
        elif lookUp[1] not in ANP_dict:
            ANP_dict[lookUp[1]] = set()
            ANP_dict[lookUp[1]].add(photoId[0])

    #---------------  CREATE QUALIFICATION -------------
    overview = Overview()
    overview.append_field("Title", "Qualification Test")
    q1_overview = Overview()
    with open('QualificationInstructions.html') as f:
        instructions="\n".join(line.strip() for line in f)
    q1_overview.append(FormattedContent(instructions))

    with open('q1.html') as f:
        img="\n".join(line.strip() for line in f)
    q1_overview.append(FormattedContent(img))

    qc1 = QuestionContent()
    qc1.append_field('Title', 'The above 10 images are related to the ANP \'amazing food\'. What emotions are related to these images?')

    fta1 = SelectionAnswer(min=1, max=3,style='checkbox',
                      selections=ratings,
                      type='text',
                      other=False)

    q1 = Question(identifier='question1',
              content=qc1,
              answer_spec=AnswerSpecification(fta1),
              is_required=True)

    q2_overview = Overview()

    with open('q2.html') as f:
        img="\n".join(line.strip() for line in f)
    q2_overview.append(FormattedContent(img))

    qc2 = QuestionContent()
    qc2.append_field('Title', 'The above 10 images are related to the ANP \'dead flowers\'. What emotions are related to these images?')

    fta2 = SelectionAnswer(min=1, max=3,style='checkbox',
                      selections=ratings,
                      type='text',
                      other=False)

    q2 = Question(identifier='question2',
              content=qc2,
              answer_spec=AnswerSpecification(fta2),
              is_required=True)

    q3_overview = Overview()

    with open('q3.html') as f:
        img="\n".join(line.strip() for line in f)
    q3_overview.append(FormattedContent(img))

    qc3 = QuestionContent()
    qc3.append_field('Title', 'The above 10 images are related to the ANP \'old buses\'. What emotions are related to these images?')

    fta3 = SelectionAnswer(min=1, max=3,style='checkbox',
                      selections=ratings,
                      type='text',
                      other=False)

    q3 = Question(identifier='question3',
              content=qc3,
              answer_spec=AnswerSpecification(fta3),
              is_required=True)

    q4_overview = Overview()

    with open('q4.html') as f:
        img="\n".join(line.strip() for line in f)
    q4_overview.append(FormattedContent(img))

    qc4 = QuestionContent()
    qc4.append_field('Title', 'The above 10 images are related to the ANP \'severe storm\'. What emotions are related to these images?')

    fta4 = SelectionAnswer(min=1, max=3,style='checkbox',
                      selections=ratings,
                      type='text',
                      other=False)

    q4 = Question(identifier='question4',
              content=qc4,
              answer_spec=AnswerSpecification(fta4),
              is_required=True)

    q5_overview = Overview()

    with open('q5.html') as f:
        img="\n".join(line.strip() for line in f)
    q5_overview.append(FormattedContent(img))

    qc5 = QuestionContent()
    qc5.append_field('Title', 'The above 10 images are related to the ANP \'abandoned house\'. What emotions are related to these images?')

    fta5 = SelectionAnswer(min=1, max=3,style='checkbox',
                      selections=ratings,
                      type='text',
                      other=False)

    q5 = Question(identifier='question5',
              content=qc5,
              answer_spec=AnswerSpecification(fta5),
              is_required=True)

    ques_form = QuestionForm()
    ques_form.append(overview)
    ques_form.append(q1_overview)
    ques_form.append(q1)
    ques_form.append(q2_overview)
    ques_form.append(q2)
    ques_form.append(q3_overview)
    ques_form.append(q3)
    ques_form.append(q4_overview)
    ques_form.append(q4)
    ques_form.append(q5_overview)
    ques_form.append(q5)

    with open('AnswerKey.xml') as f:
        ans_key="\n".join(line.strip() for line in f)

    qual_name="Qualification_Test_26"
    qual_type=mtc.create_qualification_type(name=qual_name,
                                        description="A qualification for our HITs",
                                        status="Active",
                                        retry_delay=60*5,
                                        keywords=keywords,
                                        test=ques_form,
                                        answer_key=ans_key,
                                        test_duration=1800)

    qual_id = qual_type[0].QualificationTypeId

    req = Requirement(qualification_type_id=qual_id,
                  comparator="GreaterThanOrEqualTo",
                  integer_value=3)

    # Add qualification test
    qual = Qualifications()
    qual.add(req)

    #---------------  BUILD OVERVIEW -------------------
    layoutParams= []
    hit_anp_dict= {}

    for ANP in ANP_dict:
        urls = []
        userId = []
        numImages = 0
        while numImages < 10:
            photoId = random.sample(ANP_dict[ANP],1)
            print photoId[0]
            try:
                flickrclient.photos_getPerms(photo_id=photoId[0])
            except flickrapi.exceptions.FlickrError:
                print 'Photo not available'
            else:
                try:
                    photoInfo = flickrclient.photos_getInfo(photo_id=photoId[0])
                except:
                    print 'Exception caught'
                else:
                    photoTag = photoInfo.find('photo')
                    nsId = photoInfo.find('photo/owner').attrib['nsid']
                    if nsId not in userId:
                        userId.append(nsId)
                        url = "http://farm%s.static.flickr.com/%s/%s_%s.jpg" % (photoTag.attrib['farm'], photoTag.attrib['server'], photoTag.attrib['id'], photoTag.attrib['secret'])
                        print url
                        urls.append(url)
                        numImages += 1
        name = 'image'
        namePairs = [name+`i` for i in range(1,11)]
        params = []
        anp = ANP.split('_')
        adj = anp[0]
        noun = anp[1]
        params.append(LayoutParameter('ANP', adj+' '+noun))
        for i in range(0,10):
            params.append(LayoutParameter(namePairs[i], urls[i]))

        layoutParams = LayoutParameters(params)

        #--------------- CREATE THE HIT -------------------
        my_hit = mtc.create_hit(max_assignments=3,
                                title=title,
                                description=description,
                                hit_layout='3PW3WN9P6SUZN7RDVP0586D7JDBBDM',
                                layout_params=layoutParams,
                                keywords=keywords,
                                duration = 60*60,
                                reward=0.05,
                                qualifications=qual,
                                response_groups = ['Minimal'])

        hit_id = my_hit[0].HITId

        hit_generated = mtc.get_hit(hit_id)
        if hit_id not in hit_anp_dict:
            hit_anp_dict[hit_id] = ANP
        else:
            print 'Error for Hit Id [%s] and ANP [%s]' % (hit_id, ANP)

    with open('dict.csv', 'w') as f:
        [f.write('{0},{1}\n'.format(key, value)) for key, value in hit_anp_dict.items()]

    print 'HITs posted successfully'
