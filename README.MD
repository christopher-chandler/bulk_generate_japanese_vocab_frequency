<div id="top"></div>

<!-- PROJECT SHIELDS -->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/christopher-chandler/Bulk_Generate_Japanese_Vocab_Frequency">
    <img src="readme_img/logo.png" alt="Logo" width="80" height="80">
  </a>

![Version][Version-shield]  [![MIT License][license-shield]][license-url] ![update][update-shield]

[![Stargazers][stars-shield]][stars-url]

![Windows][windows-shield] ![Mac][Mac-shield]


<h3 align="center">Bulk Generate Japanese Vocab Frequency</h3>

  <p align="center">
    Add frequency to Japanese vocab cards
    <br />
    <br />
    <a href="https://github.com/christopher-chandler/Bulk_Generate_Japanese_Vocab_Frequency/issues">Report Bug</a>
    ·
    <a href="https://github.com/christopher-chandler/Bulk_Generate_Japanese_Vocab_Frequency/issues">Request Feature</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

<div align="center">
  <a href="https://github.com/christopher-chandler/Bulk_Generate_Japanese_Vocab_Frequency">
    <img src="readme_img/logo.png" alt="Logo" width="80" height="80">
  </a>
</div>
<p align="right">(<a href="#top">back to top</a>)</p>

This add-on will generate the frequency ranking for the provided Japanese vocab field 
The frequency ranking is generated from the same frequency database of the 
Rikai-Sama,i.e., JMDict  firefox add-on.

### Built With

This project is written in pure python and the respective Anki libraries.
  ```
anki~=2.1.54
aqt~=2.1.54
  ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get to started, you have to install the add-on through Anki.
You can also install it via the files provided on Github.


### Prerequisites

You must set the variables of the  ```config.json```

```
{
    "freq_dict": "",
    "01_note_type": "Japanese",
    "02_vocab_input_field": "Target Word",
    "03_frequency_output_field": "Frequency Ranking",
    "04_overwrite_destination_field": true
}
```

* ```freq_dict```: The path of the frequency dictionary. 
It is coupled with the add-on and is located in the project directory.
You only need to copy the path of the standard dictionary or the one you provide.
* ```01_note_type``` The name of the note type which contains the vocab for which the frequency rate should be determined.
* ```02_vocab_input_field``` The field that contains the target word
* ```"03_frequency_output_field"``` The field where frequency rating should be saved.
* ```04_overwrite_destination_field``` Overwrite frequency value of the output filed (automatically set to true)


### Installation

There are two ways to install this add-on:
* Add the add-on via anki using the code ```1004691625```
* Install the add-on via the files provided on Github.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

For example, if you have a card with the vocab ``頬杖``,
then the frequency ranking of "14962" will be appended to the chosen destination field.

### What does this frequency number mean?

* If a word has a frequency of 1563, it means that 1562 words are more frequent than it. 
* Frequency number 1-5000 = very common, 5001-10000 = common, 10001-20000 = rare, 20001+ = very rare
* Frequencies are based on analysis of 5000+ novels. Naturally, frequency based on other mediums (such as newspapers) might vary.
* Not all words have frequency information. It is possible for multiple words to share the same frequency.

* More info in Rikai-Sama Add-on or its frequency ranking can be found on 
* his site at http://rikaisama.sourceforge.net/
* You can also reference to the original project https://ankiweb.net/shared/info/1612642956

### Vocab field format

The following things will be ignored when querying the frequency of a vocab:

* HTML tags (it is possible to color or format the vocab field)

<p align="right">(<a href="#top">back to top</a>)</p>

# Example

1) open the Anki-add on and insert the data into the necessary fields.
![](readme_img/config.png)

2) Go to the cards that correspond to the data you entered.
![](readme_img/card_type.png)


3) Highlight the cards that should have their frequency fields filled.
![](readme_img/insert_data.png)
4) Then open the `Edit` menu in the browser menu and click on `Bulk Generate Japanese Frequency `
![](readme_img/start_message.png)
![](readme_img/data_entered.png)

* Frequency from a colored vocab field
![](readme_img/colored_vocab.png)

<!-- ROADMAP -->
## Roadmap

- [ ] Add Jmdict support


See the [open issues](https://github.com/christopher-chandler/Bulk_Generate_Japanese_Vocab_Frequency/issues) for a full list of proposed 
features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. 
Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. 
You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

The licensing information of the project upon which
this add-on is based.

  ```
For those asking for the License permission, 
it's WTFPL. So please feel free to modify/re-upload 
a better version whenever you like.
  ```

Therefore, this project is distributed 
under the MIT License. See `LICENSE.txt` 
for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Christopher Chandler - christopher.chandler@outlook.de

Project Link: [https://github.com/christopher-chandler/Bulk_Generate_Japanese_Vocab_Frequency](https://github.com/christopher-chandler/Bulk_Generate_Japanese_Vocab_Frequency)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* @author: Myxoma (original creator)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/christopher-chandler/Bulk_Generate_Japanese_Vocab_Frequency?color=green&logoColor=%20
[contributors-url]: https://github.com/christopher-chandler/Bulk_Generate_Japanese_Vocab_Frequency/graphs/contributors

[stars-shield]: https://img.shields.io/github/stars/christopher-chandler/Bulk_Generate_Japanese_Vocab_Frequency?logoColor=yellow&style=social
[stars-url]: https://github.com/christopher-chandler/Bulk_Generate_Japanese_Vocab_Frequency/stargazers

[license-shield]: https://img.shields.io/github/license/christopher-chandler/Bulk_Generate_Japanese_Vocab_Frequency?color=yellow
[license-url]: https://github.com/christopher-chandler/Bulk_Generate_Japanese_Vocab_Frequency/blob/master/LICENSE.txt

[download-shield]: https://img.shields.io/github/downloads/christopher-chandler/Bulk_Generate_Japanese_Vocab_Frequency/total

[windows-shield]:  https://img.shields.io/badge/Windows-Tested-purple 
[mac-shield]: https://img.shields.io/badge/Mac-Tested-purple
[version-shield]: https://img.shields.io/badge/Version-1.0.0-brightgreen
[update-shield]: https://img.shields.io/badge/Last_Updated-09_2022-blue
