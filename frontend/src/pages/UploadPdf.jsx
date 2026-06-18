import { useState } from "react";
import api from "../services/api";

function UploadPdf() {

    const [file, setFile] = useState(null);

    const uploadFile = async () => {

        const formData = new FormData();

        formData.append(
            "file",
            file
        );

        try {

            const response =
                await api.post(
                    "/upload",
                    formData
                );

            alert(
                response.data.message
            );

        } catch (error) {

            console.log(error);

            alert("Upload Failed");
        }
    };

    return (

        <div>

            <h1>
                Upload PDF
            </h1>

            <input
                type="file"
                onChange={(e) =>
                    setFile(
                        e.target.files[0]
                    )
                }
            />

            <br />
            <br />

            <button
                onClick={uploadFile}
            >
                Upload
            </button>

        </div>
    );
}

export default UploadPdf;