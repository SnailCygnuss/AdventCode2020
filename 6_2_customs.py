def count_same_answers(answers_group):
    common_answers = set(answers_group[0])
    for ans in answers_group[1:]:
        ans_single = set(ans)
        common_answers = common_answers.intersection(ans_single)
        if not common_answers:
            break
    # print(common_answers)
    return len(common_answers)


def main():
    file_name = 'Day_6/6_test.txt'
    file_name = 'Day_6/6_input.txt'

    with open(file_name, 'r') as f:
        answer_count = []
        group = []
        for line in f:
            if line == '\n':
                # Call function to count answers
                answer_count.append(count_same_answers(group))
                group = []
            else:
                group.append(line.strip())
    answer_count.append(count_same_answers(group))

    print(sum(answer_count))


if __name__ == '__main__':
    main()
