// let T = document.getElementById("masterTable");
let T = document.getElementsByTagName("table")[0];
let rows = T.getElementsByTagName("tr");

let divMenu = document.createElement("div");
document.body.insertBefore(divMenu,
    document.body.firstChild);



let indexToFeature = {};
let featureToIndex = {};
let list_of_menus  = [];
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

for(let [index, dict] of Object.entries(D))
{
    let title = indexToFeature[index];
    let dropdown = document.createElement("select");
    let span = document.createElement("span");
    let space = "&nbsp;";
    let n_spaces = 3;
    let big_space = "";
    for(let i = 0; i < n_spaces; i++)
    {
        big_space += space;
    }
    span.innerHTML = big_space + title;
    divMenu.appendChild(span);
    obj_id = title + "Menu";
    dropdown.setAttribute("name", title);
    dropdown.addEventListener("input", filterTable);
    let option = document.createElement("option");
    option.value = "All";
    option.innerHTML = "All";
    dropdown.appendChild(option);
    for (let[key, _] of Object.entries(dict))
    {
        let option = document.createElement("option");
        option.value = key;
        option.innerHTML = key;
        dropdown.appendChild(option);
    }
    divMenu.appendChild(dropdown);
    list_of_menus.push(dropdown);
}

// filterTable();

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