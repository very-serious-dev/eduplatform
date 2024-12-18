import { useState, useEffect } from "react";
import EduAPIFetch from "../../client/EduAPIFetch";
import LoadingHUDPage from "./LoadingHUDPage";
import ErrorPage from "./ErrorPage";
import ClassesBody from "../components/classes/ClassesBody";

const ClassesPage = () => {
    const [classes, setClasses] = useState([]);
    const [isRequestFailed, setRequestFailed] = useState(false);
    const [requestErrorMessage, setRequestErrorMessage] = useState();
    const [isLoading, setLoading] = useState(true);
    const [newlyCreatedClasses, setNewlyCreatedClasses] = useState(0);

    useEffect(() => {
        EduAPIFetch("GET", "/api/v1/classes")
            .then(json => {
                setLoading(false);
                setClasses(json.classes);
            })
            .catch(error => {
                setLoading(false);
                setRequestFailed(true);
                setRequestErrorMessage(error.error ?? "Se ha producido un error");
            })
    }, [newlyCreatedClasses]);

    const onClassAdded = () => {
        setNewlyCreatedClasses(newlyCreatedClasses+1);
    }

    return isLoading ?
            <LoadingHUDPage />
            : isRequestFailed ?
                <ErrorPage errorMessage={requestErrorMessage} />
                : <ClassesBody classes={classes} onClassAdded={onClassAdded}/>
}

export default ClassesPage;