import urllib2
import re

import time

class NYLottery(object):
    def __init__(self):
        # Simply parsing the main page for the lottery numbers is not possible
        # with lotto, sweet million, take5, numbers, win4, quickdraw, and pick10.
        self.games = {
            "megamillions":self.getMegaMillionsNumbers,
            "powerball":self.getPowerBallNumbers,
            "lotto":self.getLottoNumbers,
            "sweetmillion":self.getSweetMillionNumbers,
            "take5":self.getTake5Numbers,
            "numbers":self.getNumbersNumbers,
            "win4":self.getWin4Numbers,
            "quickdraw":self.getQuickDrawNumbers,
            "pick10":self.getPick10Numbers
        }

    def getNumbers(self, game, date, drawtime=None):
        game = game.lower().replace(" ","")
        try:
            # Validates the date
            time.strptime(date,"%Y%m%d")
            if game == "numbers" or game == "win4":
                return self.games[game](date, drawtime)
            else:
                return self.games[game](date)
        except ValueError:
            return "Not a valid date."

    def getMegaMillionsNumbers(self, date):
        # Pages have the results of the last four years for some reason.
        # At least I won't have to find the 'next page' url.
        resultsPage = urllib2.urlopen("http://nylottery.ny.gov/wps/portal/DrawingResults?selectedGame=megamillions").read()
        resultsPage = resultsPage.replace("\t","").replace("\r","").replace("\n","")
        resultsPage = re.split("<div class=\"test\" id=\"pageNavPosition\"></div>", resultsPage)[0]
        resultsPage = re.split("/wps/portal/.*?/\">", resultsPage)[2:]
        results = {}
        for i in resultsPage:
            regexResult = re.search("(January|February|March|April|May|June|July|August|September|October|November|December) (\d\d|\d), (\d\d\d\d) MEGA MILLIONS WINNING NUMBERS: (\d\d|\d)-(\d\d|\d)-(\d\d|\d)-(\d\d|\d)-(\d\d|\d) \+ MEGA BALL  \( (\d\d|\d\s) \) MEGAPLIER x (\d|NA)",i)
            resultIndex = "".join(
                str(regexResult.group(3))+
                # Year
                str(time.strptime(regexResult.group(1)[:3],"%b").tm_mon).zfill(2)+
                # Month
                str(regexResult.group(2)).zfill(2)
                # Date
            )
            results[resultIndex] = regexResult.group(4,5,6,7,8,9)
            if resultIndex == date:
                break
        try:
            return " ".join(results[date])
        except KeyError:
            return "No drawings on that date."

    def getPowerBallNumbers(self, date):
        resultsPage = urllib2.urlopen("http://nylottery.ny.gov/wps/portal/DrawingResults?selectedGame=powerball").read()
        resultsPage = resultsPage.replace("\t","").replace("\r","").replace("\n","")
        resultsPage = re.split("<div class=\"test\" id=\"pageNavPosition\"></div>", resultsPage)[0]
        resultsPage = re.split("/wps/portal/.*?/\">", resultsPage)[2:]
        results = {}
        for i in resultsPage:
            regexResult = re.search("(January|February|March|April|May|June|July|August|September|October|November|December) (\d\d|\d), (\d\d\d\d) POWERBALL WINNING NUMBERS:(\d\d|\d)-(\d\d|\d)-(\d\d|\d)-(\d\d|\d)-(\d\d|\d) \+ POWER BALL \((\d\d|\d\s)\)",i)
            resultIndex = "".join(
                str(regexResult.group(3))+
                # Year
                str(time.strptime(regexResult.group(1)[:3],"%b").tm_mon).zfill(2)+
                # Month
                str(regexResult.group(2)).zfill(2)
                # Date
            )
            results[resultIndex] = regexResult.group(4,5,6,7,8,9)
            if resultIndex == date:
                break
        try:
            return " ".join(results[date])
        except KeyError:
            return "No drawings on that date."

    def getLottoNumbers(self, date):
        resultsPage = urllib2.urlopen("http://nylottery.ny.gov/wps/portal/DrawingResults?selectedGame=lotto").read()
        resultsPage = resultsPage.replace("\t","").replace("\r","").replace("\n","")
        resultsPage = re.split("<div class=\"test\" id=\"pageNavPosition\"></div>", resultsPage)[0]
        resultsPage = re.split("<a style=\"text-decoration:none;\" href=\"", resultsPage)[1:]
        results = {}
        for i in resultsPage:
            regexResult = re.search("(/wps/portal/.*?/)\">\W?(January|February|March|April|May|June|July|August|September|October|November|December) (\d\d|\d), (\d\d\d\d) LOTTO Drawing",i)
            resultIndex = "".join(
                str(regexResult.group(4))+
                # Year
                str(time.strptime(regexResult.group(2)[:3],"%b").tm_mon).zfill(2)+
                # Month
                str(regexResult.group(3)).zfill(2)
                # Date
            )
            # This is an URL because it needs to go to another page to retrieve the lottery numbers
            results[resultIndex] = regexResult.group(1)
            if resultIndex == date:
                # We now have the url of the page with the lottery numbers
                break
        resultsPage = urllib2.urlopen("http://nylottery.ny.gov"+results[resultIndex]).read()
        regexResult = re.search("LOTTO Winning Numbers: (\d\d|\d)-(\d\d|\d)-(\d\d|\d)-(\d\d|\d)-(\d\d|\d)-(\d\d|\d) BONUS NUMBER : (\d\d|\d)", resultsPage)
        try:
            return " ".join(regexResult.group(1,2,3,4,5,6,7))
        except AttributeError:
            return "No drawings on that date."

    def getSweetMillionNumbers(self, date):
        resultsPage = urllib2.urlopen("http://nylottery.ny.gov/wps/portal/DrawingResults?selectedGame=sweetmillion").read()
        resultsPage = resultsPage.replace("\t","").replace("\r","").replace("\n","")
        resultsPage = re.split("<div class=\"test\" id=\"pageNavPosition\"></div>", resultsPage)[0]
        resultsPage = re.split("<a style=\"text-decoration:none;\" href=\"", resultsPage)[1:]
        results = {}
        for i in resultsPage:
            regexResult = re.search("(/wps/portal/.*?/)\">\W{0,}(January|February|March|April|May|June|July|August|September|October|November|December) (\d\d|\d), (\d\d\d\d) Sweet Million Drawing",i)
            resultIndex = "".join(
                str(regexResult.group(4))+
                # Year
                str(time.strptime(regexResult.group(2)[:3],"%b").tm_mon).zfill(2)+
                # Month
                str(regexResult.group(3)).zfill(2)
                # Date
            )
            # This is an URL because it needs to go to another page to retrieve the lottery numbers
            results[resultIndex] = regexResult.group(1)
            if resultIndex == date:
                # We now have the url of the page with the lottery numbers
                break
        resultsPage = urllib2.urlopen("http://nylottery.ny.gov"+results[resultIndex]).read()
        regexResult = re.search("Sweet Million Winning Numbers: (\d\d|\d)-(\d\d|\d)-(\d\d|\d)-(\d\d|\d)-(\d\d|\d)-(\d\d|\d) Sweet Million Drawing", resultsPage)
        try:
            return " ".join(regexResult.group(1,2,3,4,5,6))
        except AttributeError:
            return "No drawings on that date."

    def getTake5Numbers(self, date):
        resultsPage = urllib2.urlopen("http://nylottery.ny.gov/wps/portal/DrawingResults?selectedGame=take5").read()
        resultsPage = resultsPage.replace("\t","").replace("\r","").replace("\n","")
        resultsPage = re.split("<div class=\"test\" id=\"pageNavPosition\"></div>", resultsPage)[0]
        resultsPage = re.split("<a style=\"text-decoration:none;\" href=\"", resultsPage)[1:]
        results = {}
        for i in resultsPage:
            regexResult = re.search("(/wps/portal/.*?/)\">\s{0,}(January|February|March|April|May|June|July|August|September|October|November|December) (\d\d|\d), (\d\d\d\d) Take Five Drawing",i)
            resultIndex = "".join(
                str(regexResult.group(4))+
                # Year
                str(time.strptime(regexResult.group(2)[:3],"%b").tm_mon).zfill(2)+
                # Month
                str(regexResult.group(3)).zfill(2)
                # Date
            )
            # This is an URL because it needs to go to another page to retrieve the lottery numbers
            results[resultIndex] = regexResult.group(1)
            if resultIndex == date:
                # We now have the url of the page with the lottery numbers
                break
        resultsPage = urllib2.urlopen("http://nylottery.ny.gov"+results[resultIndex]).read()
        resultsPage = resultsPage.replace("\t","").replace("\r","").replace("\n","")
        regexResult = re.search("Take Five Winning Numbers:\s?(\d\d|\d)-(\d\d|\d)-(\d\d|\d)-(\d\d|\d)-(\d\d|\d)\s{0,}Take Five Drawing", resultsPage)
        try:
            return " ".join(regexResult.group(1,2,3,4,5))
        except AttributeError:
            return "No drawings on that date."

    def getNumbersNumbers(self, date, drawtime):
        # Because it doesn't work:
        return "Not yet implemented"
        
        if drawtime.lower() == "midday":
            drawtime = "Midday"
        elif drawtime.lower() == "evening":
            drawtime = "Evening"
        else:
            return "Unknown draw time specified"
        resultsPage = urllib2.urlopen("http://nylottery.ny.gov/wps/portal/DrawingResults?selectedGame=numbers").read()
        resultsPage = resultsPage.replace("\t","").replace("\r","").replace("\n","")
        resultsPage = re.split("<div class=\"test\" id=\"pageNavPosition\"></div>", resultsPage)[0]
        resultsPage = re.split("<a style=\"text-decoration:none;\" href=\"", resultsPage)[1:]
        results = {}
        # Something's broken here...
        searchString = "(/wps/portal/.*?/)\">(January|February|March|April|May|June|July|August|September|October|November|December) (\d\d|\d), (\d\d\d\d)\s{0,}NUMBERS " + drawtime + " Payouts"
        for i in resultsPage:
            regexResult = re.search(searchString,i)
            resultIndex = "".join(
               str(regexResult.group(4))+
               # Year
               str(time.strptime(regexResult.group(2)[:3],"%b").tm_mon).zfill(2)+
               # Month
               str(regexResult.group(3)).zfill(2)
               # Date
            )
            # This is an URL because it needs to go to another page to retrieve the lottery numbers
            results[resultIndex] = regexResult.group(1)
            if resultIndex == date:
               # We now have the url of the page with the lottery numbers
               break
        resultsPage = urllib2.urlopen("http://nylottery.ny.gov"+results[resultIndex]).read()
        resultsPage = resultsPage.replace("\t","").replace("\r","").replace("\n","")
        regexResult1 = re.search("<td><b>(\d{1,})</b></td>", resultsPage)
        try:
            return " ".join(regexResult1.group(1))
        except AttributeError:
            return "No drawings on that date."

    def getWin4Numbers(self, date):
        # Win4 is midday/evening, too, so I'll do this one once I fix Numbers
        return "Not yet implemented"
        
    def getQuickDrawNumbers(self, date):
        # They don't even seem to have the numbers on the page.
        # Then again, it's drawn every four minutes.
        return "Not yet implemented"
        
    def getPick10Numbers(self, date):
        # These aren't on the page, either, even though it's daily.
        return "Not yet implemented"

if __name__ == "__main__":
    Lottery = NYLottery()
    print("Games available: megamillions, powerball, lotto, sweetmillion, take5")
    game = raw_input("Game: ")
    if game == "numbers" or game == "win4":
       drawtime = raw_input("Draw time: ")
    date = raw_input("Date (YYYYMMDD) (Hit Enter for today): ")
    date = time.strftime("%Y%m%d",time.gmtime()) if date == "" else date
    print(Lottery.getNumbers(game, date, drawtime=None))
