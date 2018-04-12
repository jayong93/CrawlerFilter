import argparse
import json

def add_arguments(arg_parser):
    arg_parser.add_argument("archive", nargs="+", type=argparse.FileType('r', encoding='utf-8'), help="archives to be filtered")
    arg_parser.add_argument("--like_count", type=int, default=500, help="minimum count of comment's like")
    arg_parser.add_argument("--like_ratio", type=float, default=1, help="minimum ratio of comment's like and dislike")
    arg_parser.add_argument("--dislike_multiplier", type=float, default=10, help="a number to be multiply to dislike count")
    arg_parser.add_argument("-o", "--out_to", type=argparse.FileType('w', encoding='utf-8'), help="a file to include this program's output") 
    return arg_parser

# 걸러진 댓글들을 반환하는 함수
def get_filtered_list(archive_file, min_like, min_like_ratio, dislike_multiplier):
    archive_dict = json.load(archive_file)
    main_article = archive_dict["text"]
    comment_list = get_comment_list(archive_dict)
    filtered = filter(is_useful(min_like, min_like_ratio, dislike_multiplier), comment_list)
    return {"main":main_article, "comments":[cmt["text"] for cmt in filtered]}

# 전체 기록에서 댓글만 반환하는 함수
def get_comment_list(archive_dict):
    return archive_dict["comment"].values()

# 댓글이 기준에 만족하는지 확인하는 함수를 반환하는 함수
def is_useful(min_like, min_like_ratio, dislike_multiplier):
    def is_useful_comment(comment):
        return comment["like"] >= min_like and (comment["like"]/(comment["dislike"]*dislike_multiplier)) >= min_like_ratio

    return is_useful_comment

if __name__ == "__main__":
    parser = add_arguments(argparse.ArgumentParser())
    args = parser.parse_args()
    archives = args.archive
    result = [get_filtered_list(archive, args.like_count, args.like_ratio, args.dislike_multiplier) for archive in archives]
    if len(result) == 1:
        result = result[0]
    result_json = json.dumps(result, ensure_ascii=False)
    if args.out_to == None:
        print(result_json)
    else:
        args.out_to.write(result_json)

