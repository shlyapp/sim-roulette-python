from .database.tools import load_simcard
from .scripts.scripts import get_sms


def main():
    simcards = load_simcard()
    print(get_sms(simcards[0]))


if __name__ == "__main__":
    main()
