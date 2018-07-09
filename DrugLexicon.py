
#it's a lot harder to read regex then write it
from Lexicon import Lexicon
import pandas as pd
import re



class DrugLexicon(Lexicon):

    def processLine(self, line):
            splitLine = line.split("\t")
            pgkbId = splitLine[0]
            mainName = splitLine[1]
            prelimOtherNames = []
            otherNames = []

            prelimOtherNames.append(splitLine[2])
            prelimOtherNames.append(splitLine[3])

            for name in prelimOtherNames:
                if name != '':
                    for names in name.split(','):
                        otherNames.append(names.replace('"',''))
            print(mainName)
            print(pgkbId)
            print(otherNames)
            self.addLineDataToMaps(mainName, pgkbId, otherNames, None);




    def readFromInputStream(self, lexiconInputStream):
        with open(lexiconInputStream) as fp:
            lines = fp.readlines()
            try:
                for inputLine in lines[1:]:
                    self.processLine(inputLine)
            except:
                print("file reading error")




            #both matcher parts literally just regex to parse drugs out of Generic Names and Trade Names
            #basically reading shit in line by line and then parsing out names 
            #need to figure out   addLineDataToMaps(mainName, pgkbId, otherNames, null);

drugs = DrugLexicon()
drugs.readFromInputStream('drugs.tsv')

'''
package lexicon;

// input file is PharmGKB drug lexicon

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class DrugLexicon extends Lexicon {
    private final Pattern findPattern = Pattern.compile("(?>[^,'\"]++|(['\"])(?>[^\"'\\\\]++|\\\\.|(?!\\1)[\"'])*\\1|(?<=,|^)\\s*(?=,|$))+", Pattern.DOTALL);

    public DrugLexicon(InputStream inputStream) throws IOException {
        this.readFromInputStream(inputStream);
    }

    private void processLine(String line) {
        String[] splitLine = line.split("\t");
        String pgkbId = splitLine[0];
        String mainName = splitLine[1];
        List<String> otherNames = new ArrayList<>();
        Matcher matcher = findPattern.matcher(splitLine[2].replaceAll("\"\"", "\"")); // other generic names
        while (matcher.find()) {
            // eliminate quotation marks from string ends
            String finalString = matcher.group().replaceAll("^\"|\"$", "");
            otherNames.add(finalString);
        }
        Matcher matcher2 = findPattern.matcher(splitLine[3].replaceAll("\"\"", "\"")); // trade names
        while (matcher2.find()) {
            // eliminate quotation marks from string ends
            String finalString = matcher2.group().replaceAll("^\"|\"$", "");
            otherNames.add(finalString);
        }
        addLineDataToMaps(mainName, pgkbId, otherNames, null);
    }

    @Override
    void readFromInputStream(InputStream lexiconInputStream) {
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(lexiconInputStream));

        try {
            // throw away first line because it's file header
            bufferedReader.readLine();
            String inputLine = bufferedReader.readLine();
            while (inputLine != null) {
                processLine(inputLine);
                inputLine = bufferedReader.readLine();
            }
        } catch (IOException exception) {
            System.err.println("Cannot parse input stream!");
        }
    }

    public static void main(String[] args) throws IOException {
        String outputFile = args[0];

        DrugLexicon drugLexicon = new DrugLexicon(DrugLexicon.class.getResourceAsStream("/drugs.tsv"));

        PrintWriter printWriter = new PrintWriter(outputFile);
        drugLexicon.getAllTerms().forEach(s -> printWriter.println(s + "\t" + drugLexicon.getId(s)));
        printWriter.flush();
        printWriter.close();
    }
}
'''