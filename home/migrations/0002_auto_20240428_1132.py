from django.db import migrations
import random

def create_default_courses(apps, schema_editor):
    OfferedCourses = apps.get_model('home', 'OfferedCourses')
    
    # List of default course titles
    course_titles = [
        "Python Programming Masterclass",
        "Web Development Bootcamp",
        "Machine Learning Fundamentals",
        "Digital Marketing Strategy",
        "Graphic Design for Beginners",
        "Financial Analysis and Reporting",
        "Photography Essentials",
        "Mobile App Development Workshop",
        "Creative Writing Intensive",
        "Entrepreneurship 101",
    ]
    
    # List of default course descriptions
    course_descriptions = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vitae nisl ac elit pretium scelerisque. Phasellus ac dui a magna fermentum tincidunt. Integer ultrices, nisl sit amet tempus tempus, nulla risus gravida odio, eget posuere risus orci eget sem.",
        "Fusce ullamcorper nunc ut mauris rutrum, id aliquet purus sollicitudin. Sed mattis dui at metus fermentum, nec lacinia risus malesuada. Vivamus eu odio eget quam pharetra luctus. Nulla nec interdum libero.",
        "Vestibulum nec purus vel ex ultricies auctor. Nullam pharetra tristique sapien, nec tempus ex dignissim vel. Duis ut est velit. Morbi fermentum purus ac ante convallis, nec condimentum justo vulputate.",
        "Proin eget elit vitae elit rutrum volutpat vel non ligula. Ut convallis nisl nec nibh fermentum, ac sagittis elit hendrerit. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.",
        "Aliquam erat volutpat. Nam nec orci auctor, tincidunt nisi vel, eleifend neque. Curabitur at ex arcu. Donec vitae enim eget sem auctor dapibus. Morbi lacinia, eros eu gravida iaculis, mi elit tincidunt dui, eget pharetra risus turpis non justo.",
        "Nunc vitae consectetur elit. Maecenas vel volutpat sapien. Fusce mollis nec mauris nec convallis. Nam sodales, orci eget venenatis malesuada, nisi libero rhoncus orci, id consequat mi arcu vel turpis.",
        "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Curabitur accumsan, nulla nec facilisis efficitur, neque elit condimentum nulla, ut euismod eros purus eu libero.",
        "Integer a neque nec augue consectetur bibendum. In non elit eget libero luctus efficitur eu at neque. Cras vestibulum sem a metus rutrum, vitae luctus turpis vehicula.",
        "Aenean at nulla non ligula pharetra congue ut nec tortor. Fusce vel aliquet libero. Cras suscipit sapien sit amet enim molestie, in pharetra ligula hendrerit.",
        "Phasellus nec metus sed nisi placerat dapibus. Suspendisse at consequat neque. Sed vestibulum ligula sit amet elit faucibus, nec tristique nisi aliquet.",
    ]
    
    # 10 default courses
    for _ in range(10):
        title = random.choice(course_titles)
        description = random.choice(course_descriptions)
        amount = round(random.uniform(100, 1000), 2)
        duration = f"{random.randint(2, 52)} {random.choice(['weeks', 'months', 'days'])}"
        
        OfferedCourses.objects.create(
            course_title=title,
            course_description=description,
            course_amount=amount,
            course_duration=duration
        )

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_courses),
    ]
