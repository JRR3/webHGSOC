let anchors = document.getElementsByTagName("a");
for (let anchor of anchors)
{
    anchor.onclick = updateCellColor;
}

let divMain = document.createElement("div");
divMain.style.width = "100%";
document.body.insertBefore(divMain,
    document.body.firstChild);

// There is only one table.
let T = document.getElementsByTagName("table")[0];
let rows = T.getElementsByTagName("tr");

let divTable = document.createElement("div");
// divTable.style.float = "left";
// divTable.style.width = "800px";
divTable.style.marginLeft = "300px";
// divTable.display = "inline-block";
divTable.appendChild(T);


// This div is going to hold the menus for each
// category.
let divMenu = document.createElement("div");
// divMenu.display = "inline-block";
divMenu.style.float = "left";
// divMenu.style.width = "100px";
divMenu.style.position = "fixed";

divMain.appendChild(divMenu);
divMain.appendChild(divTable);
// document.body.insertBefore(divMenu,
//     document.body.firstChild);

// divMenu.appendChild(T);

let indexToFeature = {};
let featureToIndex = {};
let list_of_menus  = [];

// There is only one header.
let header = T.getElementsByTagName("thead")[0];

let titles = header.getElementsByTagName("th");
let title_index = 0;
for (let title of titles)
{
    let txt = title.innerText;
    //Not all headers have text information.
    if (0 < txt.length)
    {
        indexToFeature[title_index] = txt;
        featureToIndex[txt] = title_index;
        title_index += 1;
    }
}

let n_indices = title_index;

// The following dictionary maps an index, as described
// in the following comment, to a dictionary of types
// for each category.
let D = {};

// let norm_index = 0;
// let theta_index = 1;
// let dist_index = 2;
// let nngb_index = 3;
// let ann_index = 4;

//Create dictionary of "n_indices" dictionaries.
for (let i = 0; i < n_indices; i++)
{
    D[i] = {}
}

for (let row of rows)
{
    //Note that the first row has no <td> tags
    let cells = row.getElementsByTagName("td");
    for(let [i, cell] of Object.entries(cells))
    {
        txt = cell.textContent;
        D[i][txt] = 1;
    }
}

// Create a menu (<select>) for each category.
// The options available for each category are
// given in the dictionary D[index].
for(let [index, dict] of Object.entries(D))
{

    // Separate each menu using n spaces.
    let space = "&nbsp;";
    let n_spaces = 1;
    let big_space = "";
    for(let i = 0; i < n_spaces; i++)
    {
        big_space += space;
    }

    // Include name and space before each menu.
    let span = document.createElement("span");
    let brk = document.createElement("br");
    let title = indexToFeature[index];
    span.innerHTML = big_space + title;
    // span.innerHTML = title;


    let dropdown = document.createElement("select");
    dropdown.setAttribute("name", title);
    dropdown.addEventListener("input", filterTable);

    // Create an option with all possible types.
    let option = document.createElement("option");
    option.value = "All";
    option.innerHTML = "All";
    dropdown.appendChild(option);

    // Include options based on the dictionary D[index].
    // The options are specific for each category.
    for (let[key, _] of Object.entries(dict))
    {
        let option = document.createElement("option");
        option.value = key;
        option.innerHTML = key;
        dropdown.appendChild(option);
    }
    divMenu.appendChild(dropdown);
    divMenu.appendChild(span);
    divMenu.appendChild(brk);
    list_of_menus.push(dropdown);
}

function filterTable(event)
{
    for (let [i_row,row] of Object.entries(rows))
    {
        //Note that the first row has no <td> tags.
        // if (i_row == 0)
        //     continue;

        let cells = row.getElementsByTagName("td");
        let showRow = true;
        for (let [i_cell, cell] of Object.entries(cells))
        {
            // let feature = event.currentTarget.name;
            // let index = featureToIndex[feature];

            let dropdown = list_of_menus[i_cell];
            let menuValue = dropdown.value;
            let txt = cell.textContent;

            if (menuValue === "All" || menuValue === txt)
            {
                // We are good.
            }
            else
            {
                showRow = false;
                break;
            }
        }
        if (showRow)
        {
            row.style.display = "";
        }
        else
        {
            row.style.display = "none";
        }
    }


}

function updateCellColor(event)
{
    let cell = event.currentTarget.parentNode;
    cell.style.backgroundColor = "blue";
}