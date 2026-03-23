const inputField = document.querySelector('.input-area input[type="text"]');
const sendButton = document.querySelector('.search');
const resetticketsButton = document.querySelector('.reset-tickets');
const resethotelsButton = document.querySelector('.reset-hotels');
const chatArea = document.querySelector('.chat-area');
const findedContainer = document.querySelector('.finded-container');
const emojis = document.querySelectorAll('.emoji');
let currentpage = 1;

let ticketsQuery = { origin: null, destination: null, departure_at: null, return_at: null, direct: null, error: null, type: "tickets" };
let hotelsQuery = { location: null, adults: null, children: null, checkIn: null, checkOut: null, stars: null, error: null, type: "hotels" };

function resetemojis() {
    emojis.forEach(emoji => {
        if (emoji.id === "emoji-hotels") { emoji.textContent = "🏨"; }
        else if (emoji.id === "emoji-tickets") { emoji.textContent = "🛫"; }
        else { emoji.textContent = "🚆"; }
        emoji.classList.remove("header");
        emoji.style.fontSize = '';
    });
}

function change_current_data() {
    document.getElementById("tickets_origin").textContent = ticketsQuery.origin;
    document.getElementById("tickets_destination").textContent = ticketsQuery.destination;
    document.getElementById("tickets_departure_at").textContent = ticketsQuery.departure_at;
    document.getElementById("tickets_return_at").textContent = ticketsQuery.return_at;
    document.getElementById("tickets_direct").textContent = ticketsQuery.direct;

    document.getElementById("hotels_location").textContent = hotelsQuery.location;
    document.getElementById("hotels_adults").textContent = hotelsQuery.adults;
    document.getElementById("hotels_children").textContent = hotelsQuery.children;
    document.getElementById("hotels_checkIn").textContent = hotelsQuery.checkIn;
    document.getElementById("hotels_checkOut").textContent = hotelsQuery.checkOut;
    document.getElementById("hotels_stars").textContent = hotelsQuery.stars;
}
change_current_data();
inputField.addEventListener('input', () => {
    sendButton.disabled = inputField.value.trim() === '';
});

async function get_n_show_tickets() {
    const elemDownloadMore = document.getElementById('div_download_more');
    if (elemDownloadMore) {
        elemDownloadMore.remove();
    };
    const ticketResponse = await fetch('/api/tickets', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({...ticketsQuery, page: currentpage}),
    });
    const ticketData = await ticketResponse.json();
    console.log(ticketData);
    if (Array.isArray(ticketData.bot_response)) {
        ticketData.bot_response.forEach(ticket => {
            const ticketDiv = document.createElement('div');
            ticketDiv.className = 'finded';
            ticketDiv.innerHTML = `
                <div class="finded-info"><span>Стоимость:</span> <span>${ticket.price}</span></div>
                <div class="finded-info"><span>Авиакомпания:</span> <span>${ticket.airline}</span></div>
                <div class="finded-info"><span>Дата вылета:</span> <span>${ticket.departure_at}</span></div>
                <div class="finded-info"><span>Дата возврата</span> <span>${ticket.return_at}</span></div>
                <div class="finded-info"><span>Откуда:</span> <span>${ticket.origin}</span></div>
                <div class="finded-info"><span>Куда:</span> <span>${ticket.destination}</span></div>
                <div class="finded-info"><span>Количество пересадок туда:</span> <span>${ticket.transfers}</span></div>
                <div class="finded-info"><span>Количество пересадок обратно:</span> <span>${ticket.return_transfers}</span></div>
                <div class="finded-info"><span>Ссылка:</span> <span><a href="${ticket.link}">БИЛЕТ</a></span></div>
            `;
            findedContainer.appendChild(ticketDiv);
        });
        const moreDiv = document.createElement('div');
        moreDiv.className = 'finded';
        moreDiv.id = 'div_download_more';
        moreDiv.innerHTML = `<span>Ссылка:</span> <span><button id="btn_more">Загрузить ещё</button></span>`;
        findedContainer.appendChild(moreDiv);
        document.getElementById('btn_more').addEventListener('click', function() {
            currentpage++;
            get_n_show_tickets();
        });
    } else if (typeof ticketData.bot_response === 'string') {
        const header = document.createElement('h3');
        header.textContent = ticketData.bot_response;
        findedContainer.appendChild(header);
    }
};

async function get_n_show_hotels() {
    const elemDownloadMore = document.getElementById('div_download_more');
    if (elemDownloadMore) {
        elemDownloadMore.remove();
    };
    const hotelsResponse = await fetch('/api/hotels', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({...hotelsQuery, page: currentpage}),
    });
    const hotelsData = await hotelsResponse.json();
    hotelsData.bot_response.forEach(hotel => {
        const existingHotel = findedContainer.querySelector(`[data-hotel-link="${hotel.link}"]`);
        if (!existingHotel) {
            const hotelDiv = document.createElement('div');
            hotelDiv.className = 'finded';
            hotelDiv.setAttribute('data-hotel-link', hotel.link);
            hotelDiv.innerHTML = `
                <div class="finded-info"><span>Отель:</span> <span>${hotel.hotelName}</span></div>
                <div class="finded-info"><span>Количество звезд:</span> <span>${hotel.stars}</span></div>
                <div class="finded-info"><span>Минимальная цена за проживание:</span> <span>${hotel.priceFrom}</span></div>
                <div class="finded-info"><span>Средняя цена за проживание:</span> <span>${hotel.priceAvg}</span></div>
                <div class="finded-info"><span>Ссылка:</span> <span><a href="${hotel.link}">ОТЕЛЬ</a></span></div>
            `;
            findedContainer.appendChild(hotelDiv);
        };
    });
    if (currentpage < 4) {
        const moreDiv = document.createElement('div');
        moreDiv.className = 'finded';
        moreDiv.id = 'div_download_more';
        moreDiv.innerHTML = `<span>Ссылка:</span> <span><button id="btn_more">Загрузить ещё</button></span>`;
        findedContainer.appendChild(moreDiv);
        document.getElementById('btn_more').addEventListener('click', function() {
            currentpage++;
            get_n_show_hotels();
        });
    };
};

resethotelsButton.addEventListener('click', async () => {
    hotelsQuery = { location: null, adults: null, children: null, checkIn: null, checkOut: null, stars: null, error: null, type: "hotels" };
    change_current_data();
});

resetticketsButton.addEventListener('click', async () => {
    ticketsQuery = { origin: null, destination: null, departure_at: null, return_at: null, direct: null, error: null, type: "tickets" };
    change_current_data();
});

sendButton.addEventListener('click', async () => {
    const userQuestion = inputField.value.trim();
    findedContainer.innerHTML = '';
    currentpage = 1;
    resethotelsButton.disabled = true;
    resetticketsButton.disabled = true;
    if (!userQuestion) return;

    inputField.value = '';
    inputField.disabled = true;
    sendButton.disabled = true;

    const userQuestionDiv = document.createElement('div');
    userQuestionDiv.className = 'user-question';
    userQuestionDiv.textContent = `Вы: ${userQuestion}`;
    chatArea.appendChild(userQuestionDiv);
    resetemojis();
    let targetEmoji = null;

    try {
        const response = await fetch('/api/question', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userQuestion, ticketscontext: ticketsQuery, hotelscontext: hotelsQuery  }),
        });
        const data = await response.json();
        
        if (data.error) {
            const botAnswerDiv = document.createElement('div');
            botAnswerDiv.className = 'bot-answer';
            botAnswerDiv.textContent = `Бот: ${data.error}`;
            chatArea.appendChild(botAnswerDiv);

            inputField.disabled = false;
            sendButton.disabled = false;
            return;
        }
    
        if (data.type === "tickets"){
            targetEmoji = document.getElementById("emoji-tickets");
            ticketsQuery = { ...ticketsQuery, ...data };
            change_current_data();
            const { origin, destination, departure_at, return_at, direct } = ticketsQuery;
            let responseText = "Бот: Ищу билеты";
            if (origin) {responseText += ` из ${origin}`;}
            if (destination) {responseText += ` в ${destination}`;}
            if (departure_at) {responseText += ` с датой отправления ${departure_at}`;}
            if (return_at) {responseText += ` и датой возврата ${return_at}`;}
            if (direct !== null) {responseText += direct ? " без пересадок" : " с пересадками";}

            const botAnswerDiv = document.createElement('div');
            botAnswerDiv.className = 'bot-answer';
            botAnswerDiv.textContent = responseText;
            chatArea.appendChild(botAnswerDiv);

            await get_n_show_tickets();
        }
        else {
            targetEmoji = document.getElementById("emoji-hotels");
            hotelsQuery = { ...hotelsQuery, ...data };
            change_current_data();
            const { location, adults, children, checkIn, checkOut, stars } = hotelsQuery;
            let responseText = "Бот: Ищу отели";
            if (location) {responseText += ` в ${location}`;}
            if (adults) {responseText += ` на ${adults} взрослых`;}
            if (children) {responseText += ` и на ${children} детей`;}
            if (checkIn) {responseText += ` с датой заселения ${checkIn}`;}
            if (checkOut) {responseText += ` и датой выселения ${checkOut}`;}
            if (stars) {responseText += ` и количеством звезд ${stars}`;}

            const botAnswerDiv = document.createElement('div');
            botAnswerDiv.className = 'bot-answer';
            botAnswerDiv.textContent = responseText;
            chatArea.appendChild(botAnswerDiv);

            await get_n_show_hotels();
        };
        if (targetEmoji && data) {
            targetEmoji.style.fontSize = '0px';
            setTimeout(() => {
                if (data.type === "tickets") {
                    targetEmoji.textContent = "Найденные авиабилеты";
                } else if (data.type === "hotels") {
                    targetEmoji.textContent = "Найденные отели";
                } else if (data.type === "trains") {
                    targetEmoji.textContent = "Найденные РЖД билеты";
                }
                targetEmoji.classList.add("header");
                targetEmoji.style.fontSize = '';
            }, 500);
        }
    } catch (error) {
        resetemojis();
        const botAnswerDiv = document.createElement('div');
        botAnswerDiv.className = 'bot-answer';
        botAnswerDiv.textContent = `Бот: Произошла ошибка. Попробуйте позже.`;
        chatArea.appendChild(botAnswerDiv);
    } finally {
        inputField.disabled = false;
        sendButton.disabled = false;
        resethotelsButton.disabled = false;
        resetticketsButton.disabled = false;
    }
    
});