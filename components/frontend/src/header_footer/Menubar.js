import React, { useState } from 'react';
import { Button, Container, Form, Header, Icon, Image, Input, Menu, Modal } from 'semantic-ui-react';
import { DateInput } from 'semantic-ui-calendar-react';

function Login(props) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  return (
    <Modal trigger={<Button secondary><Icon name='user' />Login</Button>} size='tiny'>
      <Header content='Login' />
      <Modal.Content>
        <Form onSubmit={() => props.login(username, password)}>
          <Form.Input autoFocus label='Username' name='username' onChange={(event, { name, value }) => setUsername(value)} />
          <Form.Input type='password' label='Password' name='password' onChange={(event, { name, value }) => setPassword(value)} />
          <Form.Button>Submit</Form.Button>
        </Form>
      </Modal.Content>
    </Modal>
  )
}

function Logout(props) {
  return (
    <Button secondary onClick={props.logout}><Icon name='user' />Logout {props.user}</Button>
  )
}

export function Menubar(props) {
  const today = new Date();
  const today_string = today.getDate() + '-' + (today.getMonth() + 1) + '-' + today.getFullYear();
  return (
    <Menu fixed='top' inverted>
      <Container fluid>
        <Menu.Item header onClick={(e) => props.go_home(e)}>
          <Image size='mini' src='/favicon.ico' />
        </Menu.Item>
        <Menu.Item>
          <font size="+3">Quality-time</font>
        </Menu.Item>
        <Menu.Menu position='right'>
          <Menu.Item>
            <Input icon='search' iconPosition='left' placeholder='Search...' onChange={props.onSearch} />
          </Menu.Item>
          <Menu.Item>
            <DateInput name="report_date_string" value={props.report_date_string}
              placeholder={today_string} closable={true} initialDate={today}
              maxDate={today} iconPosition="left" onChange={props.onDate} />
          </Menu.Item>
          <Menu.Item>
            {(props.user !== null) ? <Logout user={props.user} logout={props.logout} /> : <Login login={props.login} />}
          </Menu.Item>
        </Menu.Menu>
      </Container>
    </Menu>
  )
}