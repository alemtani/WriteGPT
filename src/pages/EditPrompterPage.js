import { useState, useEffect, useRef } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { useNavigate } from 'react-router-dom';
import Body from '../components/Body';
import InputField from '../components/InputField';
import { useApi } from '../contexts/ApiProvider';
import { useUser } from '../contexts/UserProvider';
import { useFlash } from '../contexts/FlashProvider';

export default function EditPrompterPage() {
    const [formErrors, setFormErrors] = useState({});
    const usernameField = useRef();
    const emailField = useRef();
    const aboutMeField = useRef();
    const api = useApi();
    const { user, setUser } = useUser();
    const flash = useFlash();
    const navigate = useNavigate();

    useEffect(() => {
        usernameField.current.value = user.username;
        emailField.current.value = user.email;
        aboutMeField.current.value = user.about_me;
        usernameField.current.focus();
    }, [user]);

    const onSubmit = async (e) => {
        e.preventDefault();
        const username = usernameField.current.value;
        const email = emailField.current.value;
        const about_me = aboutMeField.current.value;

        const errors = {};
        if (!username) {
            errors.username = 'Username must not be empty.'
        }
        if (!email) {
            errors.email = 'Email address must not be empty.'
        }
        setFormErrors(errors);
        if (Object.keys(errors).length > 0) {
            return;
        }

        const response = await api.put(`/prompters/${user.id}`, {
            username,
            email,
            about_me,
        });
        if (response.ok) {
            setFormErrors({});
            setUser(response.body);
            flash('Your profile has been updated.', 'success');
            navigate(`/prompter/${response.body.id}`);
        } else {
            flash(response.body.message, 'danger');
        }
    };

    return (
        <Body sidebar={true}>
            <Form onSubmit={onSubmit}>
                <InputField
                    name="username" label="Username"
                    error={formErrors.username} fieldRef={usernameField} />
                <InputField
                    name="email" label="Email" type="email"
                    error={formErrors.email} fieldRef={emailField} />
                <InputField
                    name="aboutMe" label="About Me"
                    error={formErrors.about_me} fieldRef={aboutMeField} />
                <Button variant="primary" type="submit">Save</Button>
            </Form>
        </Body>
    )
}