import csv

diseases = []
buckets = []
last_disease = ""
switch = True

with open("dataset_clean1.csv", "r", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    bucket = []

    for row in reader:
        disease = row[0]
        if disease != last_disease or switch:
            last_disease = disease

            if not switch:
                buckets.append(bucket)
            print(bucket)
            bucket = [row[1]]
            switch = False
        else:
            bucket.append(row[1])

with open("buckets.csv", "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile)

    for bucket in buckets:
        writer.writerow(bucket)
