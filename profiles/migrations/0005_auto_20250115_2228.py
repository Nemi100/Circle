from django.db import migrations, models

def create_initial_data(apps, schema_editor):
    SkillCategory = apps.get_model('profiles', 'SkillCategory')
    Skill = apps.get_model('profiles', 'Skill')

    # Creating categories
    software_dev = SkillCategory.objects.create(name='Software Development')
    data_science = SkillCategory.objects.create(name='Data Science')
    design = SkillCategory.objects.create(name='Design')

    # Creating skills
    skills = [
        Skill(name='Backend Developer', category=software_dev),
        Skill(name='Frontend Developer', category=software_dev),
        Skill(name='Full-Stack Developer', category=software_dev),
        Skill(name='Mobile Developer', category=software_dev),
        Skill(name='Data Analyst', category=data_science),
        Skill(name='Data Engineer', category=data_science),
        Skill(name='Machine Learning Engineer', category=data_science),
        Skill(name='AI Specialist', category=data_science),
        Skill(name='UI/UX Designer', category=design),
        Skill(name='Graphic Designer', category=design),
        Skill(name='Product Designer', category=design),
    ]
    Skill.objects.bulk_create(skills)

class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_remove_freelancerprofile_specialty_and_more'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]
