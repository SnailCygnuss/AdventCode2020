def count_questions(answers_group):
    answers = []
    for ans in answers_group:
        ans_single = [x for x in ans]
        answers.extend(ans_single)
    # print(answers)
    answers = set(answers)
    return len(answers)


def main():
    file_name = 'Day_6/6_test.txt'
    file_name = 'Day_6/6_input.txt'

    with open(file_name, 'r') as f:
        answer_count = []
        group = []
        for line in f:
            if line == '\n':
                # Call function to count answers
                answer_count.append(count_questions(group))
                group = []
            else:
                group.append(line.strip())
    answer_count.append(count_questions(group))

    print(sum(answer_count))


if __name__ == '__main__':
    main()
