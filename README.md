# Git Sentinel
Watch multiple git repos from multiple platforms

Website: https://masfaraud.github.io/git_sentinel/

[![Contributors][contributors-shield]][contributors-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

## About The Project

![stats](https://raw.githubusercontent.com/masfaraud/git_sentinel/master/docs/images/stats.png)

Git platform like github or gitea offers ticketing and simple project management. In the case of a team working across several repositories on several platforms, it is hard to monitor all the activity.
This projects aims to merge all data from these repos to offer a dashboard to follow all devs.

## Getting Started

Deploy with docker & docker compose:

```
mkdir a_folder_for_install
cd a_folder_for_install
wget https://raw.githubusercontent.com/masfaraud/git_sentinel/master/docker-compose.yml
```

Edit the docker-compose.yml file (custom ports & passwords) and run it

```
docker-compose up -d
```


## Developement install

```
python(3) setup.py install
```

Create a config python file with database info

## Usage

See the script folder

## Roadmap

- Github reading from API to read PR, issues and milestones
- API service package in docker compose
- A web frontend to explore the data

See the ![open issues](https://github.com/masfaraud/git_sentinel/issues) for a full list of proposed features (and known issues).

## Contributing

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "feature".
Don't forget to give the project a star! Thanks again!

## License

Distributed under the LGPL License. See `LICENSE` for more information.


Project Link: [https://github.com/masfaraud/git_sentinel](https://github.com/masfaraud/git_sentinel)


[contributors-shield]: https://img.shields.io/github/contributors/masfaraud/git_sentinel.svg?style=for-the-badge
[stars-shield]: https://img.shields.io/github/stars/masfaraud/git_sentinel.svg?style=for-the-badge
[issues-shield]: https://img.shields.io/github/issues/masfaraud/git_sentinel.svg?style=for-the-badge

[contributors-url]: https://github.com/masfaraud/git_sentinel/graphs/contributors
[stars-url]: https://github.com/masfaraud/git_sentinel/stargazers
[issues-url]: https://github.com/masfaraud/git_sentinel/issues
