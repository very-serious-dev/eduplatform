import { useNavigate } from "react-router";
import AnimatedButton from "./AnimatedButton";
import { useContext, useState } from "react";
import EduAPIFetch from "../../../client/EduAPIFetch";
import { FeedbackContext } from "../../main/GlobalContainer";
import DocuAPIFetch from "../../../client/DocuAPIFetch";
import { RemoveClientCache } from "../../../client/ClientCache";

const MainHeader = (props) => {
    const [isLoadingLogout, setLoadingLogout] = useState(false);
    const navigate = useNavigate();
    const setFeedback = useContext(FeedbackContext);

    const onLogout = () => {
        if (isLoadingLogout) { return; }
        setLoadingLogout(true);
        EduAPIFetch("DELETE", "/api/v1/sessions").then(json => {
            if (json.success === true) {
                DocuAPIFetch("DELETE", "/api/v1/sessions").then(json => {
                    setLoadingLogout(false);
                    if (json.success === true) {
                        RemoveClientCache()
                        navigate("/login");
                        setFeedback({ type: "info", message: "Has cerrado tu sesión" });
                    } else {
                        setFeedback({ type: "error", message: "Se ha producido un error" });
                    }
                })
                    .catch(error => {
                        setLoadingLogout(false);
                        setFeedback({ type: "error", message: error.error ?? "Se ha producido un error" });
                    })
            } else {
                setLoadingLogout(false);
                setFeedback({ type: "error", message: "Se ha producido un error" });
            }
        })
            .catch(error => {
                setLoadingLogout(false);
                setFeedback({ type: "error", message: error.error ?? "Se ha producido un error" });
            })
    }

    return <div className="mainPageHeaderContainer">
        <img className="mainPageHeaderLogo" src="/logo_main.png" />
        {isLoadingLogout ? <p>Cerrando sesión...</p>
            : <div className="mainPageHeaderButtons">
                <AnimatedButton onClick={() => { navigate("/"); }} text="📚 Clases" />
                <AnimatedButton onClick={() => { navigate("/files"); }} text="📁 Archivos" />
                <AnimatedButton onClick={() => { alert("En construcción") }} text="✉️ Mensajes" />
                {props.showAdminLink && <AnimatedButton onClick={() => { navigate("/admin"); }} text="⚙️ Panel de administración" hiddenInMobile={true} />}
                { /* TODO: Don't show logout button if user is not logged in*/}
                <AnimatedButton onClick={onLogout} rightAligned={true} text="🏃 Salir" />
            </div>}
    </div>
}

export default MainHeader;