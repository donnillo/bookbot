from reporter import Report
from stats import word_count
from stats import character_count
from paths import BOOKS
from paths import get_book_from_args


def main():
    if (BOOK := get_book_from_args()) is not None:
        with Report(BOOKS / BOOK).set_width(30) as report:
            print(f"Analyzing book found at {report.book}")

            with report.stat(word_count) as num_of_words:
                print(f"Found {num_of_words} total words")

            with report.stat(character_count, sort=True, top=10) as char_counts:
                for char, count in char_counts.items():
                    print(f"{char}: {count}")


main()
