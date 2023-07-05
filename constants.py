DEFAULT_STYLE = '''
body {
  font-family: "PT Sans", sans-serif;
  line-height: 1.2em;
  font-size: 1em;
  overflow-wrap: break-word;
}

a:link {
  color: black;
}

img {
  object-fit: contain;
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
}

h1 {
  text-indent: 0;
  font-size: 2em;
  font-weight: 200;
  line-height: 150%;
  text-align: center;
}

h1.chapter_title {
  margin: 100px 0 0 0;
  page-break-before: always;
}

h2 {
  text-indent: 0;
  font-size: 1.5em;
  font-weight: bold;
  line-height: 135%;
  text-align: center;
}

h2.chapter_sub {
  margin: 50px 0 0 0;
  page-break-before: always;
}

h3 {
  text-indent: 0;
  text-align: left;
  font-size: 1.4em;
  font-weight: bold;
}

h4 {
  text-indent: 0;
  text-align: left;
  font-size: 1.2em;
  font-weight: bold;
}

h5 {
  text-indent: 0;
  text-align: left;
  font-size: 1.1em;
  font-weight: bold;
}

h6 {
  text-indent: 0;
  text-align: left;
  font-size: 1em;
  font-weight: bold;
}

h1, h2, h3, h4, h5, h6 {
  -webkit-hyphens: none !important;
  hyphens: none;
  page-break-after: avoid;
  page-break-inside: avoid;
}

p {
  text-indent: 1.25em;
}

hr {
  width: auto;
  text-align: left;
}
'''