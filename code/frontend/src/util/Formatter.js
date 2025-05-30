const sizeToHumanReadable = (size) => { // https://stackoverflow.com/a/63032680
    const fileSize = size.toString();
    if (fileSize.length < 7) {
        return `${Math.round(+fileSize / 1024).toFixed(2)}kb`
    }
    return `${(Math.round(+fileSize / 1024) / 1000).toFixed(2)}MB`
}

const beautifullyDisplayDateHour = (date) => {
    const dateObject = new Date(date);
    return `${('0' + dateObject.getHours()).slice(-2)}:${('0' + dateObject.getMinutes()).slice(-2)}`;
}

const footNoteDateAuthor = (originalDate, author, modificationDate) => {
    if (modificationDate) {
        const modificationDateObject = new Date(modificationDate);
        return `${author ? `${author}, ` : ""}${modificationDateObject.toLocaleDateString()} (${beautifullyDisplayDateHour(modificationDateObject)}) [modificado]` 
    } else {
        const dateObject = new Date(originalDate);
        return `${author ? `${author}, ` : ""}${dateObject.toLocaleDateString()} (${beautifullyDisplayDateHour(originalDate)})`
    }
}

const beautifullyDisplayDate = (date) => {
    const getWeekDayLiteral = (day) => {
        switch (day) {
            case 0: return "Domingo";
            case 1: return "Lunes";
            case 2: return "Martes";
            case 3: return "Miércoles";
            case 4: return "Jueves";
            case 5: return "Viernes";
            case 6: return "Sábado";
        }
    }

    const getMonthLiteral = (month) => {
        switch (month) {
            case 0: return "Enero";
            case 1: return "Febrero";
            case 2: return "Marzo";
            case 3: return "Abril";
            case 4: return "Mayo";
            case 5: return "Junio";
            case 6: return "Julio";
            case 7: return "Agosto";
            case 8: return "Septiembre";
            case 9: return "Octubre";
            case 10: return "Noviembre";
            case 11: return "Diciembre"
        }
    }

    const dateObject = new Date(date);
    return `${getWeekDayLiteral(dateObject.getDay())}, ${dateObject.getDate()} de ${getMonthLiteral(dateObject.getMonth())}`;
}

const formatNullableDueDate = (dueDate) => {
    if (dueDate === undefined || dueDate === null) {
        return "Fecha sin definir"
    }
    return beautifullyDisplayDate(dueDate);
}

const formatPseudoMarkdown = (str) => {
    // For now, just transform line breaks
    // TODO: Nice-to-have: Bold (**) and lists (- )
    return str.split('\n').map(subStr => <>{subStr}<br/></>);
}

const iconImgSrc = (mimeType) => {
    // https://developer.mozilla.org/en-US/docs/Web/HTTP/MIME_types/Common_types
    /* Creative commons icons license */
    /* TODO: Show this in the web somewhere: <a href="https://www.flaticon.com/free-icons/doc" title="doc icons">Doc icons created by Dimitry Miroliubov - Flaticon</a>*/
    if (mimeType === "application/pdf") {
        return "/small/icon_pdf.png";
    } else if (mimeType.includes("video")) {
        return "/small/icon_vid.png";
    }
    if (mimeType.includes("image")) {
        return "/small/icon_img.png";
    } else if ((mimeType === "application/msword") ||
               (mimeType === "application/vnd.openxmlformats-officedocument.wordprocessingml.document") ||
               (mimeType === "application/vnd.oasis.opendocument.text")) {
        return "/small/icon_doc.png";
    } else if ((mimeType === "application/vnd.ms-excel") ||
               (mimeType === "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") ||
               (mimeType === "application/vnd.oasis.opendocument.spreadsheet")) {
        return "/small/icon_xls.png";
    } else {
        return "/small/icon_other.png";
    }
}

const textAreaDefaultPlaceholder = "Escribe aquí...";

export { sizeToHumanReadable };
export { footNoteDateAuthor };
export { beautifullyDisplayDate };
export { beautifullyDisplayDateHour };
export { formatNullableDueDate };
export { formatPseudoMarkdown };
export { iconImgSrc };
export { textAreaDefaultPlaceholder };