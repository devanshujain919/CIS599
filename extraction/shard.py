import sys
import os
import shutil

def divide(filename, num_shards):
    with open(filename, "r") as f:
        langline = f.readline()

    write_files = []
    for i in range(num_shards):
        if not os.path.exists("shard/shard-%d" %(i)):
            os.makedirs("shard/shard-%d" %(i))
            shutil.copyfile("article-extractor.py", "shard/shard-%d/article-extractor.py" %(i))
            shutil.copyfile("backlink-extractor-2.py", "shard/shard-%d/article-extractor.py" %(i))
            with open("shard/shard-%d/run.sh" %(i), "w") as f:
                f.write("python article-extractor.py wiki-shard.txt")
                f.write("python backlink-extractor-2.py wiki-shard.txt")
        write_files.append(open("shard/shard-%d/wiki-shard.txt" %(i), "a"))
        write_files[i].write(langline)

    shard_num = 0
    with open(filename, "r") as f:
        for i, line in enumerate(f):
            if not i == 0:
                write_files[shard_num].write(line)
                shard_num = (shard_num + 1) % num_shards

    for i in range(num_shards):
        write_files[i].close()

if __name__ == "__main__":
    num_shards = sys.argv[1]
    if not num_shards.isdigit():
        print("%d: Not a proper sharding int" %(int(num_shards)))
        exit(1)
    filename = sys.argv[2]
    if not os.path.exists(filename):
        print("%s file does not exist" %(filename))
        exit(1)
    divide(filename, int(num_shards))
