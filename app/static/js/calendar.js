// DEFINITION DU NUMERO DE SEMAINE
// Returns the ISO week of the date.
Date.prototype.getWeek = function () {
    var onejan = new Date(this.getFullYear(), 0, 1);
    return Math.ceil((((this - onejan) / 86400000) + onejan.getDay() + 1) / 7);
}

let today = new Date();
let curWeek = today.getWeek();
let curMonth = today.getMonth();
let curYear = today.getFullYear();

let months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
let days = ["lundi", "mardi", "mercredi", "jeudi", "vendredi"];

showCalendar(curWeek, curYear);


function showCalendar(week, year) {
    let first = new Date(year, 0, (week*7)-1);

    let calendar = document.getElementById("calendar-body");
    calendar.innerHTML = "";
    // document.getElementById("titleSemaine").innerText = `Semaine ${week} de ${year+(week===1?1:0)}`

    let date = first.getDate();
    for (let i = 0; i < 3; i++) {
        // N° jour, matin, après-midi
        if (i === 0) {
            let dateCalc = first;
            document.getElementById("semaine-lun").innerHTML = `${dateCalc.getDate()}/${dateCalc.getMonth() + 1}/${dateCalc.getFullYear()}`;
            
            dateCalc.setDate(dateCalc.getDate() + 1);
            document.getElementById("semaine-mar").innerHTML = `${dateCalc.getDate()}/${dateCalc.getMonth() + 1}/${dateCalc.getFullYear()}`;

            dateCalc.setDate(dateCalc.getDate() + 1);
            document.getElementById("semaine-mer").innerHTML = `${dateCalc.getDate()}/${dateCalc.getMonth() + 1}/${dateCalc.getFullYear()}`;

            dateCalc.setDate(dateCalc.getDate() + 1);
            document.getElementById("semaine-jeu").innerHTML = `${dateCalc.getDate()}/${dateCalc.getMonth() + 1}/${dateCalc.getFullYear()}`;

            dateCalc.setDate(dateCalc.getDate() + 1);
            document.getElementById("semaine-ven").innerHTML = `${dateCalc.getDate()}/${dateCalc.getMonth() + 1}/${dateCalc.getFullYear()}`;
            continue;
        }


        let row = document.createElement("tr");
        row.style = "height: 20px;"
        let dateCalc = date;
        for (let j = 0; j < 6; j++) {
            let cell = document.createElement("td");
            
            if (i === 1 && j === 0) {
                // Matin
                cell.innerText = "MATIN";
            }
            else if (i === 2 && j === 0) {
                // Après-midi
                cell.innerText = "APRES-MIDI";
            }
            else {
                cell.id = `${days[j - 1]}_${i === 1 ? "matin" : "apresmidi"}`;
            }
            row.appendChild(cell);
        }
        calendar.appendChild(row);
    }
}

function prevWeek() {
    today.setDate(today.getDate() - 7);
    let curWeek = today.getWeek();
    let curMonth = today.getMonth();
    let curYear = today.getFullYear();
    showCalendar(curWeek, curYear);
}

function nextWeek() {
    today.setDate(today.getDate() + 7);
    let curWeek = today.getWeek();
    let curMonth = today.getMonth();
    let curYear = today.getFullYear();
    showCalendar(curWeek, curYear);
}