<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSS Testing ground</title>

    <link rel="stylesheet" href="/static/css/fontawesome.css">
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body class="bg-body-secondary">
    <nav id="navbar" class="nav nav-darkblue pos-sticky-top shadow">
        <div class="nav-container-left">
            <a class="nav-title" href="#">
                <i class="fas fa-book mr-1" style="font-size: 32px;"></i>
                <h2>Navbar</h2>
            </a>
            <a class="nav-item" href="#">Item 1</a>
            <a class="nav-item" href="#">Item 2</a>
            <a class="nav-item" href="#">Item 3</a>
            <div class="nav-item dropdown">
                <i class="fas fa-palette"></i>&nbsp;Dropdown
                <div class="dropdown-container-left shadow-md">
                    <h3 class="dropdown-label">Navbar color</h3>
                    <a onclick="return setNavColor('nav-primary')" href="#" class="dropdown-item">Primary</a>
                    <a onclick="return setNavColor('nav-secondary')" href="#" class="dropdown-item">Secondary</a>
                    <a onclick="return setNavColor('nav-success')" href="#" class="dropdown-item">Success</a>
                    <a onclick="return setNavColor('nav-warning')" href="#" class="dropdown-item">Warning</a>
                    <a onclick="return setNavColor('nav-danger')" href="#" class="dropdown-item">Danger</a>
                    <a onclick="return setNavColor('nav-info')" href="#" class="dropdown-item">Info</a>
                    <a onclick="return setNavColor('nav-light')" href="#" class="dropdown-item">Light</a>
                    <a onclick="return setNavColor('nav-dark')" href="#" class="dropdown-item">Dark</a>
                    <a onclick="return setNavColor('nav-pink')" href="#" class="dropdown-item">Pink</a>
                    <a onclick="return setNavColor('nav-darkblue')" href="#" class="dropdown-item">Darkblue</a>
                </div>
            </div>
        </div>
        <div class="nav-container-right">
            <input class="form-control" type="text" placeholder="Place holder"><button class="btn btn-success"><i class="fas fa-search"></i></button>
            <a class="nav-item" href="#">Item 1</a>
            <a class="nav-item" href="#">Item 2</a>
            <a class="nav-item" href="#">Item 3</a>
        </div>
    </nav>

    <!-- Headings -->
    <div class="container bg-body-info px-1 py-2 shadow">
        <h1>Heading 1</h1>
        <h2>Heading 2</h2>
        <h3>Heading 3</h3>
        <h4>Heading 4</h4>
        <h5>Heading 5</h5>
        <h6>Heading 6</h6>
        <!-- Normal text -->
        <p>Normal text: Lorem ipsum dolor sit amet consectetur adipisicing elit. Magni tenetur quis quidem. Ea cumque suscipit quae quia, officia laborum laudantium est necessitatibus fugiat nihil obcaecati placeat laboriosam provident repudiandae, adipisci eos inventore.</p>
        
        <!-- Plain card -->
        <div class="card mb-2">
            <div class="card-content">
                <p>Everything looks better when rounded</p>
                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Iure repellat commodi quidem est mollitia dolorem quibusdam nihil incidunt cumque doloremque quisquam sequi fuga ipsam libero, magnam sint dolore alias perspiciatis obcaecati. Impedit maiores blanditiis, qui ratione et reiciendis veniam harum nemo odit, doloremque aliquam amet quae facilis explicabo iure quisquam accusantium molestiae distinctio repudiandae quia. Laborum illum amet incidunt inventore? Omnis debitis voluptatibus doloribus, inventore soluta eum, aperiam tempora iste illo nihil nulla ratione nemo et deleniti, sequi iusto doloremque? Cumque tenetur beatae suscipit quam excepturi. Nulla eaque blanditiis quae, voluptatem fugiat aut veniam ipsum dolor voluptas deserunt, sequi esse.</p>
            </div>
        </div>

        <!-- Plain card with image on side -->
        <div class="card mb-2">
            <div class="card-content">
                <div class="row">
                    <div class="col-sm-3 img-container">
                        <img src="/static/img/no-image.png" alt="">
                    </div>
                    <div class="col-sm-9 px-1 text-justify">
                        <h2>Plain card with image</h2>
                        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Iure repellat commodi quidem est mollitia dolorem quibusdam nihil incidunt cumque doloremque quisquam sequi fuga ipsam libero, magnam sint dolore alias perspiciatis obcaecati. Impedit maiores blanditiis, qui ratione et reiciendis veniam harum nemo odit, doloremque aliquam amet quae facilis explicabo iure quisquam accusantium molestiae distinctio repudiandae quia. Laborum illum amet incidunt inventore? Omnis debitis voluptatibus doloribus, inventore soluta eum, aperiam tempora iste illo nihil nulla ratione nemo et deleniti, sequi iusto doloremque? Cumque tenetur beatae suscipit quam excepturi. Nulla eaque blanditiis quae, voluptatem fugiat aut veniam ipsum dolor voluptas deserunt, sequi esse.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Card with header -->
        <div class="card mb-2">
            <div class="card-header bg-primary">
                <h3>Card with header</h3>
            </div>
            <div class="card-content">
                <p>Card content</p>
                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Assumenda rerum ipsa quasi totam, praesentium suscipit dolore reiciendis quaerat ipsam voluptates eveniet deserunt pariatur, ullam necessitatibus inventore exercitationem commodi! Corporis deleniti odit delectus.</p>
            </div>
        </div>

        <!-- Card foldable -->
        <div id="foldable" class="card card-foldable mb-2">
            <div class="card-header bg-primary">
                <h3>Foldable card</h3>
                <!-- <i class="fas fa-chevron-up "></i> -->
            </div>
            <div class="card-content">
                <p>Card content</p>
                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Assumenda rerum ipsa quasi totam, praesentium suscipit dolore reiciendis quaerat ipsam voluptates eveniet deserunt pariatur, ullam necessitatibus inventore exercitationem commodi! Corporis deleniti odit delectus.</p>
            </div>
        </div>

        <!-- Inline card -->
        <div class="card-inline mb-2">
            <div class="card-header bg-primary">
                <h3>Inline card </h3>
            </div>
            <div class="card-content">
                <p>Card content</p>
                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit.</p>
            </div>
        </div>
        <div class="card-inline mb-2">
            <div class="card-header bg-darkblue">
                <h3>Inline card </h3>
            </div>
            <div class="card-content">
                <p>Card content</p>
                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Odit cupiditate perferendis sit.</p>
            </div>
        </div>

        <!-- Text styles -->
        <div class="card mb-2">
            <div class="card-header bg-success">
                <h3><i class="fas fa-palette"></i> Text style</h3>
            </div>
            <div class="card-content">
                <span class="d-iblock w-10">Normal:</span>
                <span class="fg-primary">Primary</span>
                <span class="fg-secondary">Secondary</span>
                <span class="fg-success">Success</span>
                <span class="fg-warning">Warning</span>
                <span class="fg-danger">Danger</span>
                <span class="fg-info">Info</span>
                <span class="fg-light">Light</span>
                <span class="fg-dark">Dark</span>
                <span class="fg-pink">Pink</span>
                <span class="fg-darkblue">DarkBlue</span><br>
                <span class="d-iblock w-10">Body (darker):</span>
                <span class="fg-body-primary">Primary</span>
                <span class="fg-body-secondary">Secondary</span>
                <span class="fg-body-success">Success</span>
                <span class="fg-body-warning">Warning</span>
                <span class="fg-body-danger">Danger</span>
                <span class="fg-body-info">Info</span>
                <span class="fg-body-light">Light</span>
                <span class="fg-body-dark">Dark</span>
                <span class="fg-body-pink">Pink</span>
                <span class="fg-body-darkblue">DarkBlue</span><br>
                <span class="d-iblock w-10">Text style:</span>
                <span class="text-normal">Normal</span>
                <span class="text-bold">Bold</span>
                <span class="text-italic">Italic</span>
                <span class="text-underline">Underline</span>
                <span class="text-underline text-italic text-bold">All of them</span><br>
                <br>
                WOW! <span class="fg-primary">R</span><span class="fg-info">a</span><span class="fg-success">i</span><span class="fg-warning">n</span><span class="fg-danger">b</span><span class="fg-pink">o</span><span class="fg-darkblue">w</span><!--  <span class="bg-dark">HOW GAY</span> -->
            </div>
        </div>
        <!-- Flex Column control -->
        <div class="card mb-2">
            <div class="card-header bg-info">
                <h3><i class="fas fa-cog"></i> Flex grid control</h3>
            </div>
            <div class="card-content">
                <div class="control-group">
                    <select class="form-control ml-1" name="" id="select-col">
                        <option value="-10">Col-10</option>
                        <option value="">Col-12</option>
                    </select> <div class="ml-1 d-flex vflex-center text-bold">-</div>
                    <select class="form-control ml-1" name="" id="select-size">
                        <option value="">&lt;None&gt;</option>
                        <option value="-xsm">xsm</option>
                        <option value="-sm">sm</option>
                        <option value="-md">md</option>
                        <option value="-lg">lg</option>
                        <option value="-xlg">xlg</option>
                    </select> <div class="ml-1 d-flex vflex-center text-bold">-</div>
                    <input class="form-control ml-1" style="width:50px" type="number" name="" id="input-colnum" min="1" max="10" value="2">
                    <button class="btn btn-primary ml-1" id="btn-col-10" onclick="changeCol()">Set</button>
                </div>
            </div>
        </div>
        <!-- Card header colors (also col-10 or col-12 test) -->
        <div class="row my-3">
            <!-- Primary -->
            <div class="col-10-2 changed px-1 my-1">
                <div class="card">
                    <div class="card-header bg-primary">
                        <h3>Card header Primary</h3>
                    </div>
                    <div class="card-content">
                        <p>Lorem ipsum, dolor sit amet consectetur adipisicing elit. Dolore ducimus iste quaerat quasi velit voluptatum maiores.</p>
                    </div>
                </div>
            </div>
            <!-- Secondary -->
            <div class="col-10-2 changed px-1 my-1">
                <div class="card">
                    <div class="card-header bg-secondary">
                        <h3>Card header Secondary</h3>
                    </div>
                    <div class="card-content">
                        <p>Explicabo et dicta id harum architecto doloribus atque aspernatur, magni, dignissimos blanditiis officia perferendis quasi facilis?</p>
                    </div>
                </div>
            </div>
            <!-- Success -->
            <div class="col-10-2 changed px-1 my-1">
                <div class="card">
                    <div class="card-header bg-success">
                        <h3>Card header Success</h3>
                    </div>
                    <div class="card-content">
                        <p>Voluptatem aliquam eius inventore consectetur cumque ipsum expedita. Aspernatur molestiae doloribus adipisci dolor facere quisquam consequuntur.</p>
                    </div>
                </div>
            </div>
            <!-- Warning -->
            <div class="col-10-2 changed px-1 my-1">
                <div class="card">
                    <div class="card-header bg-warning">
                        <h3>Card header Warning</h3>
                    </div>
                    <div class="card-content">
                        <p>Natus voluptas laudantium id, cum placeat consectetur quas, earum corrupti quo aperiam similique soluta reprehenderit commodi?</p>
                    </div>
                </div>
            </div>
            <!-- Danger -->
            <div class="col-10-2 changed px-1 my-1">
                <div class="card">
                    <div class="card-header bg-danger">
                        <h3>Card header Danger</h3>
                    </div>
                    <div class="card-content">
                        <p>Distinctio, quibusdam eum? In quaerat assumenda accusamus, voluptatum quis perferendis magni corporis placeat. Tempora, eveniet suscipit.</p>
                    </div>
                </div>
            </div>
            <!-- Info -->
            <div class="col-10-2 changed px-1 my-1">
                <div class="card">
                    <div class="card-header bg-info">
                        <h3>Card header Info</h3>
                    </div>
                    <div class="card-content">
                        <p>Distinctio, quibusdam eum? In quaerat assumenda accusamus, voluptatum quis perferendis magni corporis placeat. Tempora, eveniet suscipit.</p>
                    </div>
                </div>
            </div>
            <!-- Light -->
            <div class="col-10-2 changed px-1 my-1">
                <div class="card">
                    <div class="card-header bg-light">
                        <h3>Card header Light</h3>
                    </div>
                    <div class="card-content">
                        <p>Velit, possimus praesentium odit enim aliquid earum. Maxime eos beatae earum amet ullam quas dicta deleniti!</p>
                    </div>
                </div>
            </div>
            <!-- Dark -->
            <div class="col-10-2 changed px-1 my-1">
                <div class="card">
                    <div class="card-header bg-dark">
                        <h3>Card header Dark</h3>
                    </div>
                    <div class="card-content">
                        <p>Nulla ipsa cumque est? Laborum, ipsam quis? Neque ullam quasi animi nisi cum beatae accusamus suscipit.</p>
                    </div>
                </div>
            </div>
            <!-- Pink -->
            <div class="col-10-2 changed px-1 my-1">
                <div class="card">
                    <div class="card-header bg-pink">
                        <h3>Card header Pink</h3>
                    </div>
                    <div class="card-content fg-body-pink">
                        <p>Nulla ipsa cumque est? Laborum, ipsam quis? Neque ullam quasi animi nisi cum beatae accusamus suscipit.</p>
                    </div>
                </div>
            </div>
            <!-- Darkblue -->
            <div class="col-10-2 changed px-1 my-1">
                <div class="card">
                    <div class="card-header bg-darkblue">
                        <h3>Card header Darkblue</h3>
                    </div>
                    <div class="card-content">
                        <p>Nulla ipsa cumque est? Laborum, ipsam quis? Neque ullam quasi animi nisi cum beatae accusamus suscipit.</p>
                    </div>
                </div>
            </div>
        </div>
        <!-- Card header colors (also col-10 or col-12 test) with body color -->
        <div class="row my-3">
            <!-- Primary -->
            <div class="col-10-2 changed px-1 my-1">
                <div class="card">
                    <div class="card-header bg-primary">
                        <h3>Card header Primary</h3>
                    </div>
                    <div class="card-content bg-body-primary">
                        <p>Lorem ipsum, dolor sit amet consectetur adipisicing elit. Dolore ducimus iste quaerat quasi velit voluptatum maiores.</p>
                    </div>
                </div>
            </div>
            <!-- Secondary -->
            <div class="col-10-2 changed px-1 my-1">
                <div class="card">
                    <div class="card-header bg-secondary">
                        <h3>Card header Secondary</h3>
                    </div>
                    <div class="card-content bg-body-secondary">
                        <p>Explicabo et dicta id harum architecto doloribus atque aspernatur, magni, dignissimos blanditiis officia perferendis quasi facilis?</p>
                    </div>
                </div>
            </div>
            <!-- Success -->
            <div class="col-10-2 changed px-1 my-1">
                <div class="card">
                    <div class="card-header bg-success">
                        <h3>Card header Success</h3>
                    </div>
                    <div class="card-content bg-body-success">
                        <p>Voluptatem aliquam eius inventore consectetur cumque ipsum expedita. Aspernatur molestiae doloribus adipisci dolor facere quisquam consequuntur.</p>
                    </div>
                </div>
            </div>
            <!-- Warning -->
            <div class="col-10-2 changed px-1 my-1">
                <div class="card">
                    <div class="card-header bg-warning">
                        <h3>Card header Warning</h3>
                    </div>
                    <div class="card-content bg-body-warning">
                        <p>Natus voluptas laudantium id, cum placeat consectetur quas, earum corrupti quo aperiam similique soluta reprehenderit commodi?</p>
                    </div>
                </div>
            </div>
            <!-- Danger -->
            <div class="col-10-2 changed px-1 my-1">
                <div class="card">
                    <div class="card-header bg-danger">
                        <h3>Card header Danger</h3>
                    </div>
                    <div class="card-content bg-body-danger">
                        <p>Distinctio, quibusdam eum? In quaerat assumenda accusamus, voluptatum quis perferendis magni corporis placeat. Tempora, eveniet suscipit.</p>
                    </div>
                </div>
            </div>
            <!-- Info -->
            <div class="col-10-2 changed px-1 my-1">
                <div class="card">
                    <div class="card-header bg-info">
                        <h3>Card header Info</h3>
                    </div>
                    <div class="card-content bg-body-info">
                        <p>Distinctio, quibusdam eum? In quaerat assumenda accusamus, voluptatum quis perferendis magni corporis placeat. Tempora, eveniet suscipit.</p>
                    </div>
                </div>
            </div>
            <!-- Light -->
            <div class="col-10-2 changed px-1 my-1">
                <div class="card">
                    <div class="card-header bg-light">
                        <h3>Card header Light</h3>
                    </div>
                    <div class="card-content bg-body-light">
                        <p>Velit, possimus praesentium odit enim aliquid earum. Maxime eos beatae earum amet ullam quas dicta deleniti!</p>
                    </div>
                </div>
            </div>
            <!-- Dark -->
            <div class="col-10-2 changed px-1 my-1">
                <div class="card">
                    <div class="card-header bg-dark">
                        <h3>Card header Dark</h3>
                    </div>
                    <div class="card-content bg-body-dark">
                        <p>Nulla ipsa cumque est? Laborum, ipsam quis? Neque ullam quasi animi nisi cum beatae accusamus suscipit.</p>
                    </div>
                </div>
            </div>
            <!-- Pink -->
            <div class="col-10-2 changed px-1 my-1">
                <div class="card">
                    <div class="card-header bg-pink">
                        <h3>Card header Pink</h3>
                    </div>
                    <div class="card-content bg-body-pink fg-body-pink">
                        <p>Nulla ipsa cumque est? Laborum, ipsam quis? Neque ullam quasi animi nisi cum beatae accusamus suscipit.</p>
                    </div>
                </div>
            </div>
            <!-- Darkblue -->
            <div class="col-10-2 changed px-1 my-1">
                <div class="card">
                    <div class="card-header bg-darkblue">
                        <h3>Card header Darkblue</h3>
                    </div>
                    <div class="card-content bg-body-darkblue fg-body-darkblue">
                        <p>Nulla ipsa cumque est? Laborum, ipsam quis? Neque ullam quasi animi nisi cum beatae accusamus suscipit.</p>
                    </div>
                </div>
            </div>
        </div>
        <!-- Form components -->
        <div class="card card-foldable mb-2">
            <div class="card-header bg-primary">
                <h3><i class="fas fa-clipboard-list"></i> Form</h3>
            </div>
            <div class="card-content">
                <!-- Buttons -->
                <div class="mb-2">
                    <h3>Buttons</h3>
                    <button class="btn btn-primary">Button</button>
                    <button class="btn btn-secondary">Button</button>
                    <button class="btn btn-success">Button</button>
                    <button class="btn btn-warning">Button</button>
                    <button class="btn btn-danger">Button</button>
                    <button class="btn btn-info">Button</button>
                    <button class="btn btn-light">Button</button>
                    <button class="btn btn-dark">Button</button>
                    <button class="btn btn-pink">Button</button>
                    <button class="btn btn-darkblue">Button</button>
                    <button class="btn btn-success d-block w-100 mt-1">Wide Button, LOL</button>
                </div>
                <!-- Buttons outline -->
                <div class="mb-2">
                    <h3>Buttons outine</h3>
                    <button class="btn-outline btn-primary">Button</button>
                    <button class="btn-outline btn-secondary">Button</button>
                    <button class="btn-outline btn-success">Button</button>
                    <button class="btn-outline btn-warning">Button</button>
                    <button class="btn-outline btn-danger">Button</button>
                    <button class="btn-outline btn-info">Button</button>
                    <button class="btn-outline btn-light">Button</button>
                    <button class="btn-outline btn-dark">Button</button>
                    <button class="btn-outline btn-pink">Button</button>
                    <button class="btn-outline btn-darkblue">Button</button>
                    <button class="btn-outline btn-success d-block w-100 mt-1">Wide Button, LOL</button>
                </div>
                <!-- Input -->
                <div class="mt-2">
                    <h3>Input</h3>
                    <input class="form-control" type="text"> <button class="btn btn-darkblue">Button</button>
                    <input class="form-control" type="text" value="Disabled" disabled> <button class="btn btn-darkblue">Button</button>
                    <input class="form-control" type="text" value="Readonly" readonly> <button class="btn btn-darkblue">Button</button>
                    <input class="form-control" type="number"> <button class="btn btn-darkblue">Button</button>
                    <input class="form-control" type="date"> <button class="btn btn-darkblue">Button</button>
                    <input class="form-control" type="file"> <button class="btn btn-darkblue">Button</button>
                </div>
                <!-- Select -->
                <div class="mt-2">
                    <h3>Select</h3>
                    <select class="form-control" name="" id="">
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                        <option value="">Option 3</option>
                        <option value="">Option 4</option>
                        <option value="">Option 5</option>
                    </select>
                </div>
                <!-- Checkbox -->
                <div class="mt-2">
                    <h3>Checkbox</h3>
                    <input id="checkbox1" class="form-control" type="checkbox"> <label for="checkbox1">Checkbox 1</label><br>
                    <input id="checkbox2" class="form-control" type="checkbox"> <label for="checkbox2">Checkbox 2</label><br>
                    <input id="checkbox3" class="form-control" type="checkbox"> <label for="checkbox3">Checkbox 3</label><br>
                    <input id="checkbox4" class="form-control" type="checkbox"> <label for="checkbox4">Checkbox 4</label><br>
                </div>
                <!-- Radio -->
                <div class="mt-2">
                    <h3>Radio</h3>
                    <input class="form-control" type="radio" name="Radio" id="radio1"><label for="radio1">Radio 1</label><br>
                    <input class="form-control" type="radio" name="Radio" id="radio2"><label for="radio2">Radio 2</label><br>
                    <input class="form-control" type="radio" name="Radio" id="radio3"><label for="radio3">Radio 3</label><br>
                    <input class="form-control" type="radio" name="Radio" id="radio4"><label for="radio4">Radio 4</label><br>
                    <input class="form-control" type="radio" name="Radio" id="radio5"><label for="radio5">Radio 5</label><br>
                </div>
                <!-- Grouping -->
                <div class="mt-2">
                    <h3>Grouping</h3>
                    <div class="control-group mt-1">
                        <button class="btn btn-primary">1</button>
                        <button class="btn btn-primary">2</button>
                        <button class="btn btn-primary">3</button>
                        <button class="btn btn-primary">4</button>
                        <button class="btn btn-primary">5</button>
                        <button class="btn btn-primary">6</button>
                        <button class="btn btn-primary">7</button>
                    </div>
                    <div class="control-group mt-1">
                        <input type="text" class="w-50 form-control" placeholder="Useful when putting stuff in straight line">
                        <select class="form-control ml-1" name="" id="">
                            <option value="">Like this</option>
                        </select>
                        <button class="btn btn-primary ml-1">Submit</button>
                    </div>
                    <h3 class="mt-1">Grouping Rounded</h3>
                    <div class="control-group-round mt-1">
                        <button class="btn btn-primary">1</button>
                        <button class="btn btn-primary">2</button>
                        <button class="btn btn-primary">3</button>
                        <button class="btn btn-primary">4</button>
                        <button class="btn btn-primary">5</button>
                        <button class="btn btn-primary">6</button>
                        <button class="btn btn-primary">7</button>
                    </div>
                    <div class="control-group-round mt-1">
                        <input type="text" class="form-control" placeholder="Better stick them together">
                        <button class="btn btn-primary">Submit</button>
                    </div>

                    <div class="control-group-round mt-1">
                        <input class="form-control" type="text" placeholder="Or it look like this">
                        <select class="form-control ml-1" name="" id="">
                            <option value="">Still look fine tho</option>
                        </select>
                        <button class="btn btn-primary ml-1">Send</button>
                    </div>
                </div>
                <!-- Progress bar -->
                <div class="mt-2">
                    <h3>Progress bar</h3>
                    <div class="progress-bar">
                        <div class="value"></div>
                    </div>
                    <div class="progress-bar">
                        <div class="value bg-success"></div>
                    </div>
                    <div class="progress-bar">
                        <div class="value bg-warning"></div>
                    </div>
                    <div class="progress-bar" style="width:90%">
                        <div class="value bg-danger"></div>
                    </div>
                    <span>50%</span>
                </div>
            </div>
        </div>

        <!-- Async test -->
        <div class="card card-foldable mb-2">
            <div class="card-header bg-primary">
                <h3>Ajax async test</h3>
            </div>
            <div class="card-content">
                <div class="my-1"><input class="form-control w-50" type="text" name="" id="test1" readonly> <span class="fg-warning" id="stat1"></span></div>
                <div class="my-1"><input class="form-control w-50" type="text" name="" id="test2" readonly> <span class="fg-warning" id="stat2"></span></div>
                <div class="my-1"><input class="form-control w-50" type="text" name="" id="test3" readonly> <span class="fg-warning" id="stat3"></span></div>
                <button class="btn btn-info" id="getajax">Get</button> <span class="fg-warning" id="stat4"></span>
            </div>
        </div>

        <!-- More background color -->
        <div class="card card-foldable mb-2">
            <div class="card-header bg-primary">
                <h3>Extra Background colors</h3>
            </div>
            <div class="card-content">
                <div class="mb-2">
                    <h2 class="bg-primary">Primary</h2>
                    <hr>
                    <div class="row">
                        <div class="col-10-2 p-2 text-center bg-d5-primary">
                            bg-d5-primary
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d10-primary">
                            bg-d10-primary
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d15-primary">
                            bg-d15-primary
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d20-primary">
                            bg-d20-primary
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d25-primary">
                            bg-d25-primary
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-10-2 p-2 text-center bg-l5-primary">
                            bg-l5-primary
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l10-primary">
                            bg-l10-primary
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l15-primary">
                            bg-l15-primary
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l20-primary">
                            bg-l20-primary
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l25-primary">
                            bg-l25-primary
                        </div>
                    </div>
                </div>

                <div class="mb-2">
                    <h2 class="bg-secondary">Secondary</h2>
                    <hr>
                    <div class="row">
                        <div class="col-10-2 p-2 text-center bg-d5-secondary">
                            bg-d5-secondary
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d10-secondary">
                            bg-d10-secondary
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d15-secondary">
                            bg-d15-secondary
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d20-secondary">
                            bg-d20-secondary
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d25-secondary">
                            bg-d25-secondary
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-10-2 p-2 text-center bg-l5-secondary">
                            bg-l5-secondary
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l10-secondary">
                            bg-l10-secondary
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l15-secondary">
                            bg-l15-secondary
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l20-secondary">
                            bg-l20-secondary
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l25-secondary">
                            bg-l25-secondary
                        </div>
                    </div>
                </div>

                <div class="mb-2">
                    <h2 class="bg-warning">Warning</h2>
                    <hr>
                    <div class="row">
                        <div class="col-10-2 p-2 text-center bg-d5-warning">
                            bg-d5-warning
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d10-warning">
                            bg-d10-warning
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d15-warning">
                            bg-d15-warning
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d20-warning">
                            bg-d20-warning
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d25-warning">
                            bg-d25-warning
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-10-2 p-2 text-center bg-l5-warning">
                            bg-l5-warning
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l10-warning">
                            bg-l10-warning
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l15-warning">
                            bg-l15-warning
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l20-warning">
                            bg-l20-warning
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l25-warning">
                            bg-l25-warning
                        </div>
                    </div>
                </div>

                <div class="mb-2">
                    <h2 class="bg-danger">Danger</h2>
                    <hr>
                    <div class="row">
                        <div class="col-10-2 p-2 text-center bg-d5-danger">
                            bg-d5-danger
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d10-danger">
                            bg-d10-danger
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d15-danger">
                            bg-d15-danger
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d20-danger">
                            bg-d20-danger
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d25-danger">
                            bg-d25-danger
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-10-2 p-2 text-center bg-l5-danger">
                            bg-l5-danger
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l10-danger">
                            bg-l10-danger
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l15-danger">
                            bg-l15-danger
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l20-danger">
                            bg-l20-danger
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l25-danger">
                            bg-l25-danger
                        </div>
                    </div>
                </div>

                <div class="mb-2">
                    <h2 class="bg-success">Success</h2>
                    <hr>
                    <div class="row">
                        <div class="col-10-2 p-2 text-center bg-d5-success">
                            bg-d5-success
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d10-success">
                            bg-d10-success
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d15-success">
                            bg-d15-success
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d20-success">
                            bg-d20-success
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d25-success">
                            bg-d25-success
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-10-2 p-2 text-center bg-l5-success">
                            bg-l5-success
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l10-success">
                            bg-l10-success
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l15-success">
                            bg-l15-success
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l20-success">
                            bg-l20-success
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l25-success">
                            bg-l25-success
                        </div>
                    </div>
                </div>

                <div class="mb-2">
                    <h2 class="bg-info">Info</h2>
                    <div class="row">
                        <div class="col-10-2 p-2 text-center bg-d5-info">
                            bg-d5-info
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d10-info">
                            bg-d10-info
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d15-info">
                            bg-d15-info
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d20-info">
                            bg-d20-info
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d25-info">
                            bg-d25-info
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-10-2 p-2 text-center bg-l5-info">
                            bg-l5-info
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l10-info">
                            bg-l10-info
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l15-info">
                            bg-l15-info
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l20-info">
                            bg-l20-info
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l25-info">
                            bg-l25-info
                        </div>
                    </div>
                </div>

                <div class="mb-2">
                    <h2 class="bg-darkblue">Darkblue</h2>
                    <hr>
                    <div class="row">
                        <div class="col-10-2 p-2 text-center bg-d5-darkblue">
                            bg-d5-darkblue
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d10-darkblue">
                            bg-d10-darkblue
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d15-darkblue">
                            bg-d15-darkblue
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d20-darkblue">
                            bg-d20-darkblue
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d25-darkblue">
                            bg-d25-darkblue
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-10-2 p-2 text-center bg-l5-darkblue">
                            bg-l5-darkblue
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l10-darkblue">
                            bg-l10-darkblue
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l15-darkblue">
                            bg-l15-darkblue
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l20-darkblue">
                            bg-l20-darkblue
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l25-darkblue">
                            bg-l25-darkblue
                        </div>
                    </div>
                </div>

                <div class="mb-2">
                    <h2 class="bg-pink">Pink</h2>
                    <hr>
                    <div class="row">
                        <div class="col-10-2 p-2 text-center bg-d5-pink">
                            bg-d5-pink
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d10-pink">
                            bg-d10-pink
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d15-pink">
                            bg-d15-pink
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d20-pink">
                            bg-d20-pink
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d25-pink">
                            bg-d25-pink
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-10-2 p-2 text-center bg-l5-pink">
                            bg-l5-pink
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l10-pink">
                            bg-l10-pink
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l15-pink">
                            bg-l15-pink
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l20-pink">
                            bg-l20-pink
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l25-pink">
                            bg-l25-pink
                        </div>
                    </div>
                </div>

                <div class="mb-2">
                    <h2 class="bg-light">Light</h2>
                    <hr>
                    <div class="row">
                        <div class="col-10-2 p-2 text-center bg-d5-light">
                            bg-d5-light
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d10-light">
                            bg-d10-light
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d15-light">
                            bg-d15-light
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d20-light">
                            bg-d20-light
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d25-light">
                            bg-d25-light
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-10-2 p-2 text-center bg-l5-light">
                            bg-l5-light
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l10-light">
                            bg-l10-light
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l15-light">
                            bg-l15-light
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l20-light">
                            bg-l20-light
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l25-light">
                            bg-l25-light
                        </div>
                    </div>
                </div>

                <div class="mb-2">
                    <h2 class="bg-dark">Dark</h2>
                    <hr>
                    <div class="row">
                        <div class="col-10-2 p-2 text-center bg-d5-dark">
                            bg-d5-dark
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d10-dark">
                            bg-d10-dark
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d15-dark">
                            bg-d15-dark
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d20-dark">
                            bg-d20-dark
                        </div>
                        <div class="col-10-2 p-2 text-center bg-d25-dark">
                            bg-d25-dark
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-10-2 p-2 text-center bg-l5-dark">
                            bg-l5-dark
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l10-dark">
                            bg-l10-dark
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l15-dark">
                            bg-l15-dark
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l20-dark">
                            bg-l20-dark
                        </div>
                        <div class="col-10-2 p-2 text-center bg-l25-dark">
                            bg-l25-dark
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- More text color -->
        <div class="card card-foldable mb-2">
            <div class="card-header bg-primary">
                <h3>More text color</h3>
            </div>
            <div class="card-content">
                <div class="mb-1">
                    <div>
                        <span class="fg-d5-primary ">Primary</span>
                        <span class="fg-d10-primary ">Primary</span>
                        <span class="fg-d15-primary ">Primary</span>
                        <span class="fg-d20-primary ">Primary</span>
                        <span class="fg-d25-primary ">Primary</span>
                    </div>
                    <div>
                        <span class="fg-l5-primary ">Primary</span>
                        <span class="fg-l10-primary ">Primary</span>
                        <span class="fg-l15-primary ">Primary</span>
                        <span class="fg-l20-primary ">Primary</span>
                        <span class="fg-l25-primary ">Primary</span>
                    </div>
                </div>

                <div class="mb-1">
                    <div>
                        <span class="fg-d5-secondary ">Secondary</span>
                        <span class="fg-d10-secondary ">Secondary</span>
                        <span class="fg-d15-secondary ">Secondary</span>
                        <span class="fg-d20-secondary ">Secondary</span>
                        <span class="fg-d25-secondary ">Secondary</span>
                    </div>
                    <div>
                        <span class="fg-l5-secondary ">Secondary</span>
                        <span class="fg-l10-secondary ">Secondary</span>
                        <span class="fg-l15-secondary ">Secondary</span>
                        <span class="fg-l20-secondary ">Secondary</span>
                        <span class="fg-l25-secondary ">Secondary</span>
                    </div>
                </div>

                <div class="mb-1">
                    <div>
                        <span class="fg-d5-success ">Success</span>
                        <span class="fg-d10-success ">Success</span>
                        <span class="fg-d15-success ">Success</span>
                        <span class="fg-d20-success ">Success</span>
                        <span class="fg-d25-success ">Success</span>
                    </div>
                    <div>
                        <span class="fg-l5-success ">Success</span>
                        <span class="fg-l10-success ">Success</span>
                        <span class="fg-l15-success ">Success</span>
                        <span class="fg-l20-success ">Success</span>
                        <span class="fg-l25-success ">Success</span>
                    </div>
                </div>

                <div class="mb-1">
                    <div>
                        <span class="fg-d5-warning ">Warning</span>
                        <span class="fg-d10-warning ">Warning</span>
                        <span class="fg-d15-warning ">Warning</span>
                        <span class="fg-d20-warning ">Warning</span>
                        <span class="fg-d25-warning">PrimaryWarning/span>
                    </div>
                    <div>
                        <span class="fg-l5-warning ">Warning</span>
                        <span class="fg-l10-warning ">Warning</span>
                        <span class="fg-l15-warning ">Warning</span>
                        <span class="fg-l20-warning ">Warning</span>
                        <span class="fg-l25-warning ">Warning</span>
                    </div>
                </div>

                <div class="mb-1">
                    <div>
                        <span class="fg-d5-danger ">Danger</span>
                        <span class="fg-d10-danger ">Danger</span>
                        <span class="fg-d15-danger ">Danger</span>
                        <span class="fg-d20-danger ">Danger</span>
                        <span class="fg-d25-danger ">Danger</span>
                    </div>
                    <div>
                        <span class="fg-l5-danger ">Danger</span>
                        <span class="fg-l10-danger ">Danger</span>
                        <span class="fg-l15-danger ">Danger</span>
                        <span class="fg-l20-danger ">Danger</span>
                        <span class="fg-l25-danger ">Danger</span>
                    </div>
                </div>

                <div class="mb-1">
                    <div>
                        <span class="fg-d5-info ">Info</span>
                        <span class="fg-d10-info ">Info</span>
                        <span class="fg-d15-info ">Info</span>
                        <span class="fg-d20-info ">Info</span>
                        <span class="fg-d25-info ">Info</span>
                    </div>
                    <div>
                        <span class="fg-l5-info ">Info</span>
                        <span class="fg-l10-info ">Info</span>
                        <span class="fg-l15-info ">Info</span>
                        <span class="fg-l20-info ">Info</span>
                        <span class="fg-l25-info ">Info</span>
                    </div>
                </div>

                <div class="mb-1">
                    <div>
                        <span class="fg-d5-darkblue ">Darkblue</span>
                        <span class="fg-d10-darkblue ">Darkblue</span>
                        <span class="fg-d15-darkblue ">Darkblue</span>
                        <span class="fg-d20-darkblue ">Darkblue</span>
                        <span class="fg-d25-darkblue ">Darkblue</span>
                    </div>
                    <div>
                        <span class="fg-l5-darkblue ">Darkblue</span>
                        <span class="fg-l10-darkblue ">Darkblue</span>
                        <span class="fg-l15-darkblue ">Darkblue</span>
                        <span class="fg-l20-darkblue ">Darkblue</span>
                        <span class="fg-l25-darkblue ">Darkblue</span>
                    </div>
                </div>

                <div class="mb-1">
                    <div>
                        <span class="fg-d5-pink ">Pink</span>
                        <span class="fg-d10-pink ">Pink</span>
                        <span class="fg-d15-pink ">Pink</span>
                        <span class="fg-d20-pink ">Pink</span>
                        <span class="fg-d25-pink ">Pink</span>
                    </div>
                    <div>
                        <span class="fg-l5-pink ">Pink</span>
                        <span class="fg-l10-pink ">Pink</span>
                        <span class="fg-l15-pink ">Pink</span>
                        <span class="fg-l20-pink ">Pink</span>
                        <span class="fg-l25-pink ">Pink</span>
                    </div>
                </div>

                <div class="mb-1">
                    <div>
                        <span class="fg-d5-dark ">Dark</span>
                        <span class="fg-d10-dark ">Dark</span>
                        <span class="fg-d15-dark ">Dark</span>
                        <span class="fg-d20-dark ">Dark</span>
                        <span class="fg-d25-dark ">Dark</span>
                    </div>
                    <div>
                        <span class="fg-l5-dark ">Dark</span>
                        <span class="fg-l10-dark ">Dark</span>
                        <span class="fg-l15-dark ">Dark</span>
                        <span class="fg-l20-dark ">Dark</span>
                        <span class="fg-l25-dark ">Dark</span>
                    </div>
                </div>

                <div class="mb-1">
                    <div>
                        <span class="fg-d5-light ">Light</span>
                        <span class="fg-d10-light ">Light</span>
                        <span class="fg-d15-light ">Light</span>
                        <span class="fg-d20-light ">Light</span>
                        <span class="fg-d25-light ">Light</span>
                    </div>
                    <div>
                        <span class="fg-l5-light ">Light</span>
                        <span class="fg-l10-light ">Light</span>
                        <span class="fg-l15-light ">Light</span>
                        <span class="fg-l20-light ">Light</span>
                        <span class="fg-l25-light ">Light</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="/static/js/lib/jquery-3.6.0.min.js"></script>
    <script src="/static/js/test/test_css.js"></script>
</body>
</html>