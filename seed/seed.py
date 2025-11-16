import os.path
import shutil
import uuid

from sqlalchemy import func

from extentions.extensions import db,app
from models.models import Category, News

with app.app_context():
    print("Running Seed...")
    # Category
    category_list = ("បច្ចេកវិទ្យា", "កីឡា", "សង្គម", "កម្សាន្ត")
    for category in category_list:
        # check category already exist or not
        is_exist = Category.query.filter_by(name=category).first()
        if is_exist:
            print(f"Category {category} already exist.")
        else:
            db.session.add(Category(name=category))
            db.session.commit()
            print(f"Category {category} has been added.")
    # News
    news_list = [
        # ---------------------- បច្ចេកវិទ្យា ----------------------
        {
            "title": "Apple បង្ហាញ iPhone 17 Pro Max ជាមួយកាមេរ៉ា 200MP និងកម្រិត Refresh Rate 120Hz",
            "description": "Apple បានប្រកាសចេញ iPhone 17 Pro Max ថ្មី មានកាមេរ៉ាថ្មី 200MP និងបំពាក់បច្ចេកវិទ្យា Refresh Rate 120Hz សម្រាប់បទពិសោធន៍មើលរូបភាពល្អបំផុត។",
            "content": "ក្រុមហ៊ុន Apple បានប្រកាសចេញ iPhone 17 Pro Max ជាថ្មីនៅក្នុងព្រឹត្តិការណ៍ប្រចាំឆ្នាំរបស់ខ្លួន ដែលនាំមកនូវការកែលម្អខ្ពស់ទាក់ទងនឹងកាមេរ៉ា, អេក្រង់, និងថាមពលបម្រើ។ iPhone 17 Pro Max បានបំពាក់កាមេរ៉ាថ្មី 200MP ដែលអាចថតរូបមានច្បាស់ល្អ និងអាចថតវីដេអូក្នុងកម្រិត 8K, ជាមួយនឹងអាល់ហ្គរីធម៍ Smart HDR 5.0 ដែលអាចធ្វើអោយពណ៌ស្រស់ល្អ និងពន្លឺសមរម្យទាំងក្នុងថ្ងៃ និងយប់។\n\nផ្នែកខាងក្នុងប្រើ Chip A21 Bionic ជាមួយ RAM 12GB ដែលធានាថាការរត់កម្មវិធី, Game, និង Multi-tasking នឹងរលូន និងឆ្លាតវៃ។ អេក្រង់ Super Retina XDR មានកម្រិត Refresh Rate 120Hz និង Dynamic Tone Mapping ផ្តល់បទពិសោធន៍មើលវីដេអូ ឬ Game មានភាពរលូន និងពណ៌ខ្ពស់។\n\nថ្មបានបង្កើនទៅ 4500mAh និងគាំទ្រ Fast Charging 30W និង Wireless Charging 20W, អាចសាកពី 0 ទៅ 100% ក្នុងរយៈពេលស្ដង់ដារ 1.5 ម៉ោង។ ក្រុមហ៊ុន Apple បានផ្តល់ជូនម៉ូដែល Pro Max ជាមួយអង្គផ្ទុកទិន្នន័យ 1TB សម្រាប់អ្នកដែលចូលចិត្តថតវីដេអូ 8K និងរូបថតកំរិតខ្ពស់។\n\nក្រុមហ៊ុន Apple អះអាងថា iPhone 17 Pro Max នឹងផ្តល់បទពិសោធន៍ល្អប្រសើរជាងមុនសម្រាប់អ្នកប្រើប្រាស់ ទោះជា Game, Video Editing ឬ Photography ក៏ដោយ។ ការបង្ហាញនេះបង្ហាញពីភាពខ្ពស់នៃការប្រកួតប្រជែងក្នុងទីផ្សារទូរសព្ទធ្វើឲ្យក្រុមហ៊ុនមួយៗត្រូវប្រកួតប្រជែងបច្ចេកវិទ្យាថ្មីៗគ្នាទៅមុខ។",
            "category_id": 1,
            "thumbnail": "iphone17_pro_max.webp"
        },
        {
            "title": "Samsung Galaxy Z Fold 6 សំរាប់ឆ្នាំ 2026 នឹងបំពាក់ថ្មសាកលឿន 45W",
            "description": "Samsung បានផ្តល់ព័ត៌មានថា Galaxy Z Fold 6 នឹងមានថ្មសាកលឿន 45W និងចំនួនកាមេរ៉ា 4 លើខាងក្រោយ។",
            "content": "Samsung Galaxy Z Fold 6 គឺជាតម្លើងថ្មីក្នុងស៊េរី Foldable Smartphone ដែលផ្តល់បទពិសោធន៍ល្អសម្រាប់ Productivity និង Entertainment។ អេក្រង់ foldable AMOLED 7.8 inch មានកម្រិត Refresh Rate 120Hz, Dynamic AMOLED 2X ដែលអាចបង្ហាញពណ៌បានច្បាស់ និងពន្លឺខ្ពស់សម្រាប់ប្រើប្រាស់ក្រៅផ្ទះ។\n\nថ្មសាកលឿន 45W អាចសាកពី 0 ទៅ 100% ក្នុងរយៈពេល 45 នាទី និងមានថ្មទុកសម្រាប់ Standby ទៅ 2 ថ្ងៃ។ កាមេរ៉ា 4 លើខាងក្រោយរួមមាន Main 108MP, Ultra-wide 12MP, Telephoto 10MP និង Macro 5MP ដែលអាចថតរូបយ៉ាងច្បាស់ល្អ ទោះក្នុងសីតុណ្ហភាពខ្សោយ ឬក្នុងសីតុណ្ហភាពថ្ងៃចម្ងាយ។\n\nGalaxy Z Fold 6 បានប្រើ Snapdragon 9 Gen 3 ជាមួយ RAM 16GB និង Storage 1TB, មាន Android 14 ដំណើរការលើ One UI 6.0. នេះធានាថាអ្នកប្រើប្រាស់អាច multitask, Game, និង Productivity apps ដោយរលូន។\n\nលើសពីនេះ Galaxy Z Fold 6 មាន hinge design ថ្មីដែលខ្លី និងទ្រទ្រង់ជាងមុន អាចប្រើជាច្រើនលើ Desktop Mode ដើម្បីបង្កើតបទពិសោធន៍ដូចកុំព្យូទ័រ Laptop។ ស្មាតហ្វូននេះត្រូវបានទាក់ទាញជាអ្នកប្រើប្រាស់ Business និង Creator ដែលចង់ទទួលបទពិសោធន៍ foldable phone ល្អ។",
            "category_id": 1,
            "thumbnail": "galaxy_z_fold6.webp"
        },
        {
            "title": "Meta បញ្ចេញ AR Glasses ជំនាន់ថ្មីសម្រាប់ពិភព Metaverse",
            "description": "Meta បានបង្ហាញ AR Glasses ជំនាន់ថ្មី ដែលអាចបង្ហាញពិភព Metaverse និងគាំទ្រពីកម្មវិធី VR/AR ផ្សេងៗ។",
            "content": "AR Glasses ថ្មីរបស់ Meta អាចបង្ហាញ Virtual Environment និង Overlay ព័ត៌មានផ្ទាល់ខ្លួន លើភពផ្ទាល់។ វាបំពាក់សេនស័រទិដ្ឋភាព និងកាមេរ៉ា LiDAR សម្រាប់បង្កើត 3D Mapping ពិភពជុំវិញអ្នកប្រើ។ អ្នកអាចភ្ជាប់ទៅ Oculus និងកម្រិត 5G ដើម្បីទទួលបទពិសោធន៍ VR/AR រលូន។\n\nក្រុមហ៊ុន Meta បានចូលរួមជាមួយអ្នកបង្កើត Content ដើម្បីផ្តល់បទពិសោធន៍ផ្សេងៗដូចជា Virtual Meeting, Gaming, និង Social Interaction ក្នុង Metaverse។ AR Glasses នេះគាំទ្រការបង្ហាញ Real-time Information Overlay, Navigation, និង Smart Assistant ដោយស្មាតវេរ។",
            "category_id": 1,
            "thumbnail": "meta_ar_glasses.webp"
        },
        {
            "title": "Intel ប្រកាស CPU Core i13 ថ្មី សម្រាប់កុំព្យូទ័រលើ Desktop",
            "description": "Intel បានចេញ Core i13 ជំនាន់ថ្មីសម្រាប់ Desktop ដែលមាន Core 32 និង Thread 64 សម្រាប់កម្រិត Performance ខ្ពស់។",
            "content": "Intel Core i13 មាន Core 32 និង Thread 64 និង Base Clock 4.0GHz Turbo Boost 6.0GHz ផ្តល់ការរត់កម្មវិធី និងហ្គេមលឿនជាងមុន។ វាបំពាក់ PCIe 6.0 និង DDR6X Memory គាំទ្រការរីកចម្រើនលើ 3D Rendering និង Video Editing។\n\nCPU ថ្មីនេះមាន Architecture 5nm, Energy Efficient និង Support AI Accelerators សម្រាប់ការគណនា Machine Learning។ Intel បានលើកទឹកចិត្តអ្នកប្រើប្រាស់ Desktop, Creators, និង Data Analysts ដើម្បីបង្កើន Productivity និងធ្វើ Rendering Project 3D ឬ Video Project ទៅកម្រិតខ្ពស់។",
            "category_id": 1,
            "thumbnail": "intel_core_i13.webp"
        },
        {
            "title": "Xiaomi 14 Ultra មានកាមេរ៉ា 1-inch Sensor សម្រាប់ថតរូបយប់",
            "description": "Xiaomi 14 Ultra នឹងមានកាមេរ៉ា 1-inch Sensor និងថ្ម 6000mAh សម្រាប់ថតរូបយប់ និងប្រើប្រាស់បានយូរ។",
            "content": "កាមេរ៉ា 1-inch Sensor នេះអាចថតរូបយប់បានច្បាស់ និងមាន Dynamic Range ខ្ពស់។ ទូរស័ព្ទបំពាក់ថ្ម 6000mAh និងសាកលឿន 120W ធ្វើឲ្យអ្នកអាចប្រើប្រាស់បានយូរ និងសាកថ្មក្នុងពេលតូច។ Xiaomi 14 Ultra គាំទ្រកម្រិត Refresh Rate 120Hz និងកាមេរ៉ា Telephoto 10x Optical Zoom។\n\nXiaomi បានបន្ថែម AI Camera Features ដូចជា Night Mode 2.0, Portrait Pro, និង Motion Capture ដើម្បីឲ្យអ្នកថតរូប និងវីដេអូមានភាពទាក់ទាញ និងស្អាតបំផុត។ ទូរស័ព្ទនេះគាំទ្រការភ្ជាប់ 5G, Wi-Fi 7 និង Bluetooth 5.3 សម្រាប់ការផ្សព្វផ្សាយឯកសារ និង Gaming Online បានលឿន។",
            "category_id": 1,
            "thumbnail": "xiaomi14_ultra.webp"
        },

        # ---------------------- កីឡា ----------------------
        {
            "title": "Vinícius Júnior ស៊ុត Hat-Trick Real Madrid ឈ្នះ Dortmund 5-2",
            "description": "UEFA Champions League សប្តាហ៍ទី 3 Real Madrid ជួប Dortmund Vinícius Júnior ស៊ុត Hat-Trick ដាក់ Real Madrid ឈ្នះ 5-2។",
            "content": "ក្នុងជំនួប UEFA Champions League សប្តាហ៍ទី 3 រវាង Real Madrid និង Dortmund ក្រុមម្ចាស់ផ្ទះ Real Madrid បានបង្ហាញលទ្ធភាពខ្ពស់ក្រោមការដឹកនាំរបស់ Carlo Ancelotti។ Vinícius Júnior បានស៊ុត Hat-Trick ដើម្បីបញ្ចប់ជំនួបជាមួយលទ្ធផល 5-2។\n\nវគ្គទី១ Dortmund អាចដាក់គ្រាប់បាល់ 2 គ្រាប់មុនពីការលេងលឿន និងប្រើប្រាស់ Space ល្អក្នុងការវាយប្រហារ, ប៉ុន្តែវគ្គទី២ Real Madrid ប្រែជំរើសលទ្ធផលបានវិញ ដោយការបញ្ជូនបាល់យ៉ាងឆ្លាតវៃ និងការត្រួតពិនិត្យ Midfield បានសំខាន់។\n\nVinícius Júnior បានស៊ុតគ្រាប់ទី១ នៅនាទី 62 ដើម្បីស្មើគ្រាប់ 2-2, បន្ទាប់មកគ្រាប់ទី២ និងទី៣ បានកើតឡើងនៅនាទី 86 និង 90+3 បញ្ចប់ជំនួប។ Lucas Vázquez និង A. Rüdiger ក៏បានចូលរួមក្នុងការផ្គត់ផ្គង់ Goal ដើម្បីធានា Real Madrid ឈ្នះយ៉ាងច្បាស់។\n\nការឈ្នះនេះផ្តល់ពិន្ទុ 3 សម្រាប់ Real Madrid និងធ្វើឲ្យពួកគេមានស្ថានភាពល្អក្នុង Group Stage, ដោយមានភាពរីករាយសម្រាប់អ្នកគាំទ្របាល់ទាត់នៅជុំវិញពិភពលោក។",
            "category_id": 2,
            "thumbnail": "real_dortmund.webp"
        },
        {
            "title": "Messi កាន់ Ballon d'Or លើកទី 8 ក្នុងអតីតកាល",
            "description": "Lionel Messi បានទទួល Ballon d'Or លើកទី 8 បង្ហាញពីភាពអស្ចារ្យក្នុងអាជីពកីឡាបាល់ទាត់។",
            "content": "Lionel Messi បានទទួល Ballon d'Or លើកទី 8 ក្រោយការបង្ហាញសមត្ថភាពខ្ពស់ក្នុងអាជីពរបស់គាត់។ ក្នុងឆ្នាំនេះ, Messi បានបង្ហាញការលេងខ្ពស់ទាំងនៅ World Cup 2022 ជាមួយ Argentina និង Champions League 2023 ជាមួយ Paris Saint-Germain។\n\nការទទួលបាន Ballon d'Or លើកទី 8 គឺជាការបង្ហាញពីភាពអស្ចារ្យ និងការបន្តជោគជ័យរបស់ Messi នៅក្នុងប្រវត្តិសាស្ត្រ។ គាត់បានបង្ហាញភាពជាអ្នកដឹកនាំក្នុងក្រុម និងជាកីឡាករដែលមានសមត្ថភាពបង្កើតឱកាសវាយប្រហារច្រើនសម្រាប់ក្រុម។",
            "category_id": 2,
            "thumbnail": "messi_ballondor.webp"
        },
        {
            "title": "FIFA បញ្ជាក់រួចរាល់ក្របខ័ណ្ឌ World Cup 2030",
            "description": "FIFA បានធ្វើការបញ្ជាក់ប្រទេសចូលរួម និងទីកន្លែងប្រារព្ធ World Cup 2030។",
            "content": "FIFA បានប្រកាសអំពីប្រទេសដែលនឹងចូលរួមក្នុង World Cup 2030, ចំនួន 48 ប្រទេស និងទីកន្លែងប្រារព្ធនៅ Morocco, Spain, និង Portugal។ ក្របខ័ណ្ឌថ្មីនេះបានបង្កើតកម្រិតតេស្តសមត្ថភាពកីឡាករ និងផ្តល់ឱកាសចូលរួមលើក្រុមក្រុមតូចៗក្នុង World Cup។",
            "category_id": 2,
            "thumbnail": "worldcup2030.webp"
        },
        {
            "title": "NBA: LeBron James ធ្វើ Triple-Double ជាមួយ Lakers",
            "description": "LeBron James បានបង្ហាញការសម្តែងល្អក្នុងជំនួប Lakers ជាមួយ Triple-Double ជាមួយ 30 points, 12 rebounds និង 10 assists។",
            "content": "LeBron James បានធ្វើ Triple-Double ក្នុងការប្រកួត NBA ជាមួយ Los Angeles Lakers ប្រឆាំង Houston Rockets, នាំឲ្យក្រុមឈ្នះលទ្ធផល 120-110។ អ្នកគាំទ្របាល់បោះ និងអ្នកវិភាគបានសរសើរពីសមត្ថភាពដឹកនាំ និងការផ្លាស់ប្តូរបាល់យ៉ាងឆ្លាតវៃ។",
            "category_id": 2,
            "thumbnail": "lebron_triple.webp"
        },
        {
            "title": "Olympics 2024: Cambodia ស្នាក់ទី 25 ក្នុងការប្រកួតហែលទឹក",
            "description": "កីឡាករហែលទឹកកម្ពុជា បានស្នាក់ទី 25 ក្នុងការប្រកួតលើក Olympics 2024 Paris។",
            "content": "កីឡាករហែលទឹកកម្ពុជា បានប្រើពេល 54.32 វិនាទីក្នុងប្រកួត 100m Freestyle និងស្នាក់ទី 25 ក្នុងការប្រកួត Olympics 2024។ ការចូលរួមនេះបង្ហាញពីភាពខិតខំ និងការបន្តអភិវឌ្ឍន៍កីឡាករកម្ពុជា, ជាអនុស្សាវរីយ៍ដ៏ល្អសម្រាប់អ្នកវ័យក្មេង។",
            "category_id": 2,
            "thumbnail": "cambodia_olympics.webp"
        },

        # ---------------------- សង្គម ----------------------
        {
            "title": "ក្រសួងសង្គមចេញយុទ្ធនាការ​ការពារ​សិទ្ធិស្ត្រី",
            "description": "ក្រសួងសង្គមបានចេញយុទ្ធនាការការពារ​សិទ្ធិស្ត្រី និងជំរុញការស្មើភាពភេទនៅកម្ពុជា។",
            "content": "ក្រសួងសង្គមបានចាប់ផ្ដើមយុទ្ធនាការ 'សិទ្ធិស្ត្រីសម្រាប់សង្គម' ដោយមានគោលបំណងបង្កើនការយល់ដឹង និងការពារសិទ្ធិស្ត្រី។ អង្គការសហគមន៍ និងសាលា, មណ្ឌលសង្គម ត្រូវបានចូលរួមក្នុងការរៀបចំវគ្គបណ្ដុះបណ្ដាល និងសិក្ខាសាលាស្ត្រី។\n\nយុទ្ធនាការនេះក៏ផ្តោតលើការបង្កើតអាផាតមេនសម្រាប់ស្ត្រីខ្ពស់ភាពតិច និងការចូលរួមក្នុង Decision Making នៅកន្លែងការងារ, ដើម្បីធានាថាស្ត្រីមានសិទ្ធិ និងអាចចូលរួមក្នុងសង្គមបានស្មើភាព។",
            "category_id": 3,
            "thumbnail": "social_women_rights.webp"
        },
        {
            "title": "ការព្យាបាលសុខភាពចិត្ត សម្រាប់អ្នកវ័យក្មេងក្នុងកម្ពុជា",
            "description": "យុទ្ធនាការផ្តល់សេវាសុខភាពចិត្ត និងអប់រំការគ្រប់គ្រងសម្ពាធសម្រាប់យុវជនកម្ពុជា។",
            "content": "ក្រសួងសុខាភិបាល និងអង្គការសហជីពបានចាប់ផ្ដើមកម្មវិធីផ្តល់ការប្រឹក្សាសុខភាពចិត្ត, Counseling, និង Training Program សម្រាប់យុវជន។ កម្មវិធីនេះផ្តោតលើការគ្រប់គ្រងសម្ពាធ, ការលុបបំបាត់ Stress, និងការរស់នៅដោយសុខសាន្ត។ អ្នកវ័យក្មេងបានចូលរួមជាច្រើន និងរៀនពីវិធីការពារ Mental Health ក្នុងសង្គមទំនើប។",
            "category_id": 3,
            "thumbnail": "mental_health.webp"
        },
        {
            "title": "ការរីកចម្រើនសេដ្ឋកិច្ចសង្គមក្រោយកូវីដ-១៩",
            "description": "ការសិក្សាបង្ហាញថាសេដ្ឋកិច្ចសង្គមកម្ពុជា​កំពុងរីកចម្រើនយ៉ាងលឿនក្រោយវិបត្តិកូវីដ-១៩។",
            "content": "សិក្សាចុងក្រោយបានបង្ហាញថាការវិនិយោគ, ពាណិជ្ជកម្ម និងការបង្កើតកន្លែងការងារថ្មីៗ បានធ្វើឲ្យសេដ្ឋកិច្ចសង្គមកម្ពុជា រីកចម្រើនយ៉ាងលឿន។ ក្រសួងសង្គមបានចេញវិធានការផ្សេងៗដើម្បីគាំទ្រក្រុមគ្រួសារខ្សោយ, ពង្រឹងសេវាសង្គម និងបង្កើតសហគមន៍ដែលមានសុខសាន្ត។",
            "category_id": 3,
            "thumbnail": "economy_post_covid.webp"
        },
        {
            "title": "ក្រុមជំនាញអប់រំចាប់ផ្ដើមវគ្គបណ្ដុះបណ្ដាល Online សម្រាប់អ្នកចង់រៀនបន្ថែម",
            "description": "វគ្គបណ្ដុះបណ្ដាល Online បានចាប់ផ្ដើមសម្រាប់អ្នកវ័យក្មេង និងមនុស្សធំដែលចង់រៀនបន្ថែម។",
            "content": "អង្គការអប់រំ និងសាលា Online បានចាប់ផ្ដើមវគ្គបណ្ដុះបណ្ដាលជាច្រើន ដូចជា Digital Skills, Programming, និង Soft Skills។ វគ្គនេះអាចចូលរួម Online, មាន Certificate, និងផ្តល់ឱកាសបង្កើន Career Prospects សម្រាប់អ្នកចូលរួម។",
            "category_id": 3,
            "thumbnail": "online_training.webp"
        },
        {
            "title": "ការរីកចម្រើនប្រព័ន្ធសង្គមក្នុងភូមិកម្ពុជា",
            "description": "គម្រោងបង្កើត Community Center និងសេវាសង្គមនៅភូមិ កំពុងទទួលបានភាពជោគជ័យ។",
            "content": "គម្រោង Community Center នៃក្រសួងសង្គមកំពុងផ្តល់សេវាសាធារណៈដល់ប្រជាជនក្នុងភូមិ ដូចជា Health Care, Education, និង Recreation។ គម្រោងនេះបានបង្កើតឱកាសការងារសម្រាប់យុវជន, ជួយបង្កើនសេដ្ឋកិច្ចតំបន់, និងផ្សព្វផ្សាយការរួមគ្នានៃសហគមន៍។",
            "category_id": 3,
            "thumbnail": "community_center.webp"
        },

        # ---------------------- កម្សាន្ត ----------------------
        {
            "title": "Disneyland Paris បើករដូវកាលថ្មី Magical Spring 2025",
            "description": "Disneyland Paris បើករដូវកាលថ្មី Magical Spring 2025 ជាមួយព្រឹត្តិការណ៍ពិសេស និង Parade ថ្មីៗ។",
            "content": "Disneyland Paris បានប្រកាសបើករដូវកាល Magical Spring 2025 ដែលមាន Parade ថ្មីៗ, Fireworks, និង Character Meet-and-Greet ជាច្រើន។ អ្នកទស្សនាអាចរីករាយជាមួយ Disney Princesses, Marvel Superheroes និង Pixar Characters ក្នុងបរិយាកាសស្រស់ស្អាត និង Interactive Experiences។\n\nក្រុម Disneyland បានផ្តល់ពេលវេលា 2 ម៉ោងសម្រាប់ Attractions ដ៏ពេញនិយម ដូចជា Pirates of the Caribbean, Space Mountain, និង Ratatouille Adventure, ដែលអាចរីករាយបានទាំងគ្រួសារ។",
            "category_id": 4,
            "thumbnail": "disneyland_paris.webp"
        },
        {
            "title": "Marvel Studios បង្ហាញ Trailer ថ្មីសម្រាប់ Avengers: Legacy",
            "description": "Marvel Studios បានបង្ហាញ Trailer ថ្មី Avengers: Legacy ដែលនឹងចេញនៅឆ្នាំ 2025។",
            "content": "Trailer ថ្មីបានបង្ហាញភាព Action, Adventure និងតួអង្គថ្មីៗនៅក្នុង Avengers: Legacy។ Movie នេះនឹងបន្ត Universe MCU និងផ្តល់ការតភ្ជាប់ពី Phase 5 ដល់ Phase 6។ អ្នកគាំទ្រ Marvel ទាំងអស់កំពុងរង់ចាំថ្ងៃចេញចលនា ដើម្បីទស្សនាអំពី Superheroes និងកិច្ចការសង្គ្រោះពិភពលោក។",
            "category_id": 4,
            "thumbnail": "avengers_legacy.webp"
        },
        {
            "title": "Concert BTS នៅ Seoul ប្រជុំអ្នកគាំទ្រចំនួន 100,000",
            "description": "BTS បានរៀបចំ Concert នៅ Seoul ជាមួយអ្នកគាំទ្រចំនួន 100,000 នាក់។",
            "content": "Concert BTS ក្នុង Seoul បានទាក់ទាញអ្នកគាំទ្រចំនួន 100,000 នាក់ និងបានផ្តល់បទពិសោធន៍អស្ចារ្យសម្រាប់ Fans។ បទចម្រៀងថ្មីៗ, Dance Performance និង Visual Effects បានធ្វើឲ្យ Concert ក្លាយជាអត្ថប្រយោជន៍ដ៏ពិសេស។ Concert នេះគឺជាផ្នែកមួយនៃ World Tour 2025 របស់ BTS។",
            "category_id": 4,
            "thumbnail": "bts_concert.webp"
        },
        {
            "title": "Netflix ចេញ Series ថ្មី Sci-Fi The Last Galaxy",
            "description": "Netflix បានចេញ Series ថ្មី Sci-Fi The Last Galaxy ដែលមានភាព Action និង Adventure ។",
            "content": "The Last Galaxy Series នេះបានបង្ហាញពិភពអាកាសយាន និងអគ្គិសនីផ្ទាល់ខ្លួន ដែលត្រូវបានអ្នកប្រើប្រាស់ទស្សនាច្រើន។ Series មាន Plot twists, Character Development និង Visual Effects ជាច្រើនដែលធ្វើឲ្យទស្សនិកជនស្រឡាញ់។ ក្រុមអ្នកបញ្ចេញបានប្រកាសថា Season 1 មាន 10 Episodes និងចេញ Streaming នៅលើ Netflix នៅឆ្នាំ 2025។",
            "category_id": 4,
            "thumbnail": "netflix_last_galaxy.webp"
        },
        {
            "title": "Cambodia International Film Festival 2025 ចាប់ផ្ដើមជាផ្លូវការ",
            "description": "Cambodia International Film Festival 2025 បានចាប់ផ្ដើម ជាមួយភាពយន្តអន្តរជាតិ និងការប្រកួតសិល្បៈ។",
            "content": "Cambodia International Film Festival 2025 បានផ្តល់ឱកាសដល់អ្នកសិល្បៈ និង Filmmakers ពិភពលោកក្នុងការចូលរួមក្នុង Screenings, Workshops, និង Q&A Sessions។ Festival នេះក៏ផ្តល់ការទទួលស្គាល់ Award Categories ដូចជា Best Film, Best Director និង Best Actor, ជួយឱ្យ Cambodian Cinema មានភាពសក្តិសមជាងមុន។",
            "category_id": 4,
            "thumbnail": "cambodia_film_festival.webp"
        },
        {
            "title": "Disney+ បន្ថែម Feature Interactive Watch Party",
            "description": "Disney+ បានបន្ថែម Feature អ្នកប្រើអាចរីករាយ Watch Party ជាមួយមិត្តភក្តិ និងគ្រួសារ។",
            "content": "Feature Interactive Watch Party អនុញ្ញាតឱ្យអ្នកប្រើ Disney+ អាចរៀបចំការទស្សនារួមជាមួយមិត្តភក្តិ និងគ្រួសារ, Chat, និង Reactions Live។ នេះជាជំហានថ្មីក្នុង Streaming Services ដើម្បីទាក់ទាញអ្នកប្រើ និងផ្តល់បទពិសោធន៍អស្ចារ្យ។ Users អាចបង្កើត Event, Invite Friends, និង Enjoy Movies / Series Streaming យ៉ាងល្អ។",
            "category_id": 4,
            "thumbnail": "disney_plus_watchparty.webp"
        }
    ]

    for news in news_list:
        exist_news = News.query.filter_by(title=news['title']).first()
        if exist_news:
            print(f"News {news['title']} already exists")
        else:
            # thumbnail_path = os.path.join("uploads_init","news",news["thumbnail"])
            # if os.path.isfile(thumbnail_path):
            #     file_ext = news["thumbnail"].split('.')[-1]
            #     safe_filename = f"{uuid.uuid4().hex}.{file_ext}"
            #     des_path = os.path.join("uploads","news",safe_filename)
            #     if os.path.isfile(des_path):
            #         pass
            #     else:
            #         shutil.copy(thumbnail_path,des_path)
            category_id = Category.query.filter(func.lower(Category.name) == func.lower(category)).first().id
            news_item = News(
                title=news["title"],
                description=news["description"],
                content=news["content"],
                category_id=news["category_id"],
                thumbnail=news["thumbnail"],
            )
            db.session.add(news_item)
            db.session.commit()
            print(f"News {news['title']} has been added.")
            # else:
            #     print("No Thumbnail file.")