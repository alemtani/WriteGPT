import { useState, useEffect, useRef } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Body from "../components/Body";
import InputField from "../components/InputField";
import { useApi } from "../contexts/ApiProvider";
import { useFlash } from "../contexts/FlashProvider";
import { Link } from "react-router-dom";

export default function ResetRequestPage() {
    const [formErrors, setFormErrors] = useState({});
    const emailField = useRef();
    const api = useApi();
    const flash = useFlash();

    useEffect(() => {
        emailField.current.focus();
    }, []);

    const onSubmit = async (e) => {
        e.preventDefault();
        const email = emailField.current.value;

        const errors = {};
        if (!email) {
            errors.email = 'Email must not be empty.';
        }
        setFormErrors(errors);
        if (Object.keys(errors).length > 0) {
            return;
        }

        const response = await api.post('/tokens/reset', {email});
        if (!response.ok) {
            flash(response.body.message, 'danger');
        } else {
            emailField.current.value = '';
            setFormErrors({});
            flash('You will receive an email with instructions to reset your password.');
        }
    };

    return (
        <Body>
            <h1>Reset Your Password</h1>
            <Form onSubmit={onSubmit}>
                <InputField
                    name="email" label="Email Address"
                    error={formErrors.email} fieldRef={emailField} />
                <Button variant="primary" type="submit">Reset Password</Button>
            </Form>
            <hr />
            <p>All set? Go back to <Link to="/login">Login</Link>.</p>
        </Body>
    )
}