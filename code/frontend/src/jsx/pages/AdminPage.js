import { useState, useEffect } from "react";
import { EduAPIFetch } from "../../client/APIFetch";
import LoadingHUDPage from "./LoadingHUDPage";
import ErrorPage from "./ErrorPage";
import AdminBody from "../components/admin/AdminBody";

const AdminPage = () => {
    const [dashboardData, setDashboardData] = useState();
    const [isRequestFailed, setRequestFailed] = useState(false);
    const [requestErrorMessage, setRequestErrorMessage] = useState();
    const [isLoading, setLoading] = useState(true);
    const [refreshKey, setRefreshKey] = useState(0);

    useEffect(() => {
        document.title = "Panel";
    }, []);

    useEffect(() => {
        EduAPIFetch("GET", "/api/v1/admin/home")
            .then(json => {
                setLoading(false);
                setDashboardData(json);
            })
            .catch(error => {
                setLoading(false);
                setRequestFailed(true);
                setRequestErrorMessage(error.error ?? "Se ha producido un error");
            })
    }, [refreshKey])

    return isLoading ?
        <LoadingHUDPage />
        : isRequestFailed ?
            <ErrorPage errorMessage={requestErrorMessage} />
            : <AdminBody dashboardData={dashboardData}
                onShouldRefresh={() => { setRefreshKey(x => x + 1); }} />

}

export default AdminPage;